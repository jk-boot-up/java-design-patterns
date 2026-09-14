package com.jk.explore.circuitbreaker;

/**
 * Five acts. Recommendations is down in all of them; what changes is the response.
 *
 * The numbers to watch are how long the shopper waited and how many calls actually
 * reached the service that is already known to be broken.
 */
public final class CircuitBreakerDemo {

    private static final String SKU = "SKU-1234";
    private static final int FAILURES_BEFORE_OPENING = 3;
    private static final long RESET_AFTER_MILLIS = 5_000;

    public static void main(String[] args) {
        System.out.println("Circuit breaker: Recommendations has stopped answering");
        System.out.println();

        retryingAnOutage();
        theBreakerOpens();
        theBreakerRecovers();
        checkoutHasNoFallback();
        checkoutPretendsItWorked();
    }

    /** Act 1: the wrong pattern for this failure. */
    private static void retryingAnOutage() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        RecommendationsService recommendations = new RecommendationsService(clock, log).goDown();

        ProductPage page = new RetryingProductPageService(recommendations, log).page(SKU);

        System.out.println("1. Retry, applied to an outage");
        System.out.print(log.timeline());
        System.out.println("  page: " + page.summary());
        System.out.printf("  the shopper waited %dms for a page with nothing extra on it,%n",
                log.elapsedMillis());
        System.out.printf("  and a service that is already down received %d more calls.%n",
                recommendations.callsReceived());
        System.out.println();
    }

    /** Act 2: the breaker trips, and then costs nothing. */
    private static void theBreakerOpens() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        RecommendationsService recommendations = new RecommendationsService(clock, log).goDown();
        CircuitBreaker breaker = new CircuitBreaker("Recommendations", FAILURES_BEFORE_OPENING,
                RESET_AFTER_MILLIS, clock, log);
        ProductPageService pages = new ProductPageService(recommendations, breaker, log);

        for (int i = 0; i < 6; i++) {
            pages.page(SKU);
        }

        System.out.println("2. Six product pages, with a breaker");
        System.out.print(log.timeline());
        System.out.println("  6 pages served, every one of them buyable, none with suggestions");
        System.out.printf("  %d calls reached Recommendations, %d were refused without a call%n",
                breaker.callsMade(), breaker.callsRefused());
        System.out.printf("  total time %dms -- the first three shoppers paid for the outage,%n",
                log.elapsedMillis());
        System.out.println("  and everybody after them got their page instantly.");
        System.out.println();
    }

    /** Act 3: one probe, and the shop heals itself. */
    private static void theBreakerRecovers() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        RecommendationsService recommendations = new RecommendationsService(clock, log).goDown();
        CircuitBreaker breaker = new CircuitBreaker("Recommendations", FAILURES_BEFORE_OPENING,
                RESET_AFTER_MILLIS, clock, log);
        ProductPageService pages = new ProductPageService(recommendations, breaker, log);

        for (int i = 0; i < 3; i++) {
            pages.page(SKU);            // trips the breaker
        }
        pages.page(SKU);                // refused instantly
        recommendations.comeBackUp();   // the operations team fixes it
        clock.advance(RESET_AFTER_MILLIS);
        ProductPage healed = pages.page(SKU);   // the probe

        System.out.println("3. Recommendations comes back, and one probe finds out");
        System.out.print(log.timeline());
        System.out.println("  page: " + healed.summary());
        System.out.println("  state: " + breaker.state()
                + " -- nobody deployed anything to make that happen.");
        System.out.println();
    }

    /** Act 4: the same breaker where there is nothing to fall back to. */
    private static void checkoutHasNoFallback() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        PaymentsService payments = new PaymentsService(clock, log).goDown();
        CircuitBreaker breaker = new CircuitBreaker("Payments", FAILURES_BEFORE_OPENING,
                RESET_AFTER_MILLIS, clock, log);
        CheckoutService checkout = new CheckoutService(payments, breaker, log);

        int refused = 0;
        for (int i = 0; i < 5; i++) {
            try {
                checkout.pay("ORD-500" + i, Money.pence(44999));
            } catch (CheckoutUnavailableException e) {
                refused++;
            }
        }

        System.out.println("4. Checkout: the same breaker, no fallback");
        System.out.print(log.timeline());
        System.out.printf("  %d shoppers were told honestly that we cannot take payment%n", refused);
        System.out.printf("  %d cards were charged%n", payments.chargesMade());
        System.out.println("  there is no substitute for taking the money, so the breaker does not");
        System.out.println("  buy a fallback here. It buys a fast, honest 'no' instead of a spinner.");
        System.out.println();
    }

    /** Act 5: the fallback that should never be written. */
    private static void checkoutPretendsItWorked() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        PaymentsService payments = new PaymentsService(clock, log).goDown();
        CircuitBreaker breaker = new CircuitBreaker("Payments", FAILURES_BEFORE_OPENING,
                RESET_AFTER_MILLIS, clock, log);
        PretendItWorkedCheckoutService checkout =
                new PretendItWorkedCheckoutService(payments, breaker, log);

        String receipt = checkout.pay("ORD-9001", Money.pence(44999));

        System.out.println("5. The same outage, with a fallback that lies");
        System.out.print(log.timeline());
        System.out.println("  the shopper was shown receipt " + receipt + " and thanked");
        System.out.printf("  cards actually charged: %d%n", payments.chargesMade());
        System.out.println("  nothing threw, no alert fired, and the warehouse will ship an");
        System.out.println("  espresso machine nobody paid for. A fallback that hides a real");
        System.out.println("  failure is worse than the error it replaced.");
    }
}
