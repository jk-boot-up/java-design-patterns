package com.jk.explore.retry;

/**
 * Four acts on the same flaky gateway, charging the same £449.99 for the same order.
 *
 * The number to watch in every act is the last line: how many times the customer's
 * card was charged. The right answer is always one.
 */
public final class RetryDemo {

    private static final String ORDER = "ORD-5001";
    private static final Money AMOUNT = Money.pence(44999);
    private static final long SEED = 7L;

    public static void main(String[] args) {
        System.out.println("Retry with backoff: a flaky payment gateway");
        System.out.println();

        aTimeoutThatRecovers();
        aDeclinedCardIsNotRetried();
        theReplyIsLostAfterTheCardIsCharged();
        theSameLostReplyWithTheNaiveLoop();
    }

    /** Act 1: the case retrying is for. The request never arrived; the second one did. */
    private static void aTimeoutThatRecovers() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        PaymentGateway payments = new PaymentGateway(clock, log).timeOutNext(1);

        Receipt receipt = new CheckoutService(payments, RetryPolicy.threeAttempts(SEED),
                clock, log).pay(ORDER, AMOUNT);

        System.out.println("1. The gateway timed out once, then worked");
        System.out.print(log.timeline());
        System.out.println("  checkout succeeded: " + receipt);
        System.out.println("  card charged " + payments.charges().size() + " time, "
                + payments.totalCharged() + " in total");
        System.out.println();
    }

    /** Act 2: the case retrying is not for. */
    private static void aDeclinedCardIsNotRetried() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        PaymentGateway payments = new PaymentGateway(clock, log).declineAlways();

        String outcome;
        try {
            new CheckoutService(payments, RetryPolicy.threeAttempts(SEED), clock, log)
                    .pay(ORDER, AMOUNT);
            outcome = "succeeded, which it should not have";
        } catch (CardDeclinedException e) {
            outcome = "declined, and the shopper was told at once: " + e.getMessage();
        }

        System.out.println("2. The bank declined the card");
        System.out.print(log.timeline());
        System.out.println("  checkout " + outcome);
        System.out.println("  the gateway was asked " + payments.attempts()
                + " time -- a 'no' does not become a 'yes' on the third attempt");
        System.out.println();
    }

    /** Act 3: the dangerous failure, handled. */
    private static void theReplyIsLostAfterTheCardIsCharged() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        PaymentGateway payments = new PaymentGateway(clock, log).loseReplyAfterCharging(1);

        Receipt receipt = new CheckoutService(payments, RetryPolicy.threeAttempts(SEED),
                clock, log).pay(ORDER, AMOUNT);

        System.out.println("3. The card was charged and the reply was lost");
        System.out.print(log.timeline());
        System.out.println("  checkout succeeded: " + receipt);
        System.out.println("  card charged " + payments.charges().size() + " time, "
                + payments.totalCharged() + " in total");
        System.out.println("  the retry carried the same key, so the gateway recognised it and");
        System.out.println("  handed back the charge it had already made.");
        System.out.println();
    }

    /** Act 4: the same failure, the loop everybody writes first. */
    private static void theSameLostReplyWithTheNaiveLoop() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        PaymentGateway payments = new PaymentGateway(clock, log).loseReplyAfterCharging(1);

        Receipt receipt = new NaiveCheckoutService(payments, log).pay(ORDER, AMOUNT);

        System.out.println("4. The same failure, with a plain three-times loop");
        System.out.print(log.timeline());
        System.out.println("  checkout succeeded: " + receipt);
        System.out.println("  card charged " + payments.charges().size() + " times, "
                + payments.totalCharged() + " in total");
        System.out.println("  the shopper paid twice for one espresso machine. Nothing threw,");
        System.out.println("  nothing was logged as an error, and the order looks perfect.");
    }
}
