package com.jk.explore.sidecar;

import java.util.List;
import java.util.Map;

/**
 * The whole lesson, in seven acts.
 *
 * <p>Acts 1 to 3 are the problem: four services, sixteen copied decisions, and the night
 * one of those copies was left behind. Acts 4 and 5 are the pattern and what it actually
 * changes. Acts 6 and 7 are the bill, because a pattern taught without its costs is an
 * advertisement.
 *
 * <p>Every number printed below is measured, not typed. The attempt counts come from the
 * payment gateway's own log rather than from the services that made them, the timings
 * come from a clock that is moved by hand so that they are identical on every machine,
 * and the counts of copies come from arithmetic over the services that exist.
 */
public final class PaymentsDemo {

    private static final Payment SUBSCRIPTION = Payment.of("SUB-90118", 1299);
    private static final Payment CHECKOUT = Payment.of("ORD-4417", 4799);
    private static final Payment REFUND = Payment.of("REF-3820", 2250);
    private static final Payment PAYOUT = Payment.of("PAY-7741", 18640);

    public static void main(String[] args) {
        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
        actSeven();
    }

    /** Four services, and the sixteen decisions none of them is about. */
    private static void actOne() {
        heading("Act 1 — four services that take money, and sixteen copies");
        PaymentGateway gateway = new PaymentGateway();
        gateway.behave();

        System.out.println("  Four parts of the shop charge a card, for four different reasons:");
        System.out.println();
        System.out.println("    checkout              a customer is watching a spinner");
        System.out.println("    refunds               the coffee maker came back");
        System.out.println("    subscription-billing  two in the morning, thousands of cards");
        System.out.println("    marketplace-payouts   paying the sellers, every Friday");
        System.out.println();
        System.out.println("  Different teams, different repositories, different release days.");
        System.out.println("  And each of them had to decide the same four things:");
        System.out.println();
        printGrid(gateway);
        System.out.println();
        System.out.println("  Sixteen values. Not one of them is about checkout, refunds,");
        System.out.println("  subscriptions or payouts. They are all facts about the network");
        System.out.println("  and the provider's contract — true whoever is making the call.");
        System.out.println();
        System.out.println("  copies of a cross-cutting decision: "
                + Concerns.copiesInsideTheServices(4));
        System.out.println("  places to edit to change one:       "
                + Concerns.placesToEditAPolicy(4));
    }

    /** The provider asks for a change. It is made in three of the four places. */
    private static void actTwo() {
        heading("Act 2 — the provider asks for a change, and it lands three times");
        PaymentGateway gateway = new PaymentGateway();
        gateway.behave();

        System.out.println("  In March the provider writes to every merchant. Retrying ten");
        System.out.println("  milliseconds after a failure does not help anybody, it only");
        System.out.println("  costs them capacity. From now on: at most three attempts per");
        System.out.println("  payment, and wait properly between them.");
        System.out.println();
        System.out.println("  An engineer opens checkout, changes two lines, ships it. Then");
        System.out.println("  refunds. Then payouts. Three pull requests, three reviews,");
        System.out.println("  three releases, all in one afternoon, and everybody goes home.");
        System.out.println();

        CheckoutService checkout = new CheckoutService(gateway);
        RefundsService refunds = new RefundsService(gateway);
        MarketplacePayoutsService payouts = new MarketplacePayoutsService(gateway);
        SubscriptionBillingService billing = new SubscriptionBillingService(gateway);
        checkout.applyPolicyReview();
        refunds.applyPolicyReview();
        payouts.applyPolicyReview();

        printGridHeader();
        printSettingsRow("checkout", checkout.settings());
        printSettingsRow("refunds", refunds.settings());
        printSettingsRow("marketplace-payouts", payouts.settings());
        printSettingsRow("subscription-billing", billing.settings());
        System.out.println();
        System.out.println("  The fourth row is the one to look at. Nobody was careless, and");
        System.out.println("  nobody was even wrong. Subscription billing runs overnight, is");
        System.out.println("  owned by another team, lives in another repository, and had no");
        System.out.println("  open work that sprint. There was no fourth place to look unless");
        System.out.println("  you already knew to look there.");
        System.out.println();
        System.out.println("  Nothing throws. Nothing is logged. Every test still passes, in");
        System.out.println("  all four services, because each one tests its own copy.");
    }

    /** The next wobble, and the service that pays for somebody else's retries. */
    private static void actThree() {
        heading("Act 3 — the next wobble, at two in the morning");
        PaymentGateway gateway = new PaymentGateway();
        CheckoutService checkout = new CheckoutService(gateway);
        RefundsService refunds = new RefundsService(gateway);
        MarketplacePayoutsService payouts = new MarketplacePayoutsService(gateway);
        checkout.applyPolicyReview();
        refunds.applyPolicyReview();
        payouts.applyPolicyReview();
        SubscriptionBillingService billing = new SubscriptionBillingService(gateway);

        System.out.println("  The gateway has a bad " + PaymentGateway.RECOVERS_AT_MILLIS
                + " milliseconds. Nothing is broken and");
        System.out.println("  nobody needs paging — it declines everything, then it is fine.");
        System.out.println("  The contract allows the shop "
                + PaymentGateway.ATTEMPTS_ALLOWED_PER_WOBBLE + " attempts across the account:");
        System.out.println("  three per payment, four services taking payments. The "
                + (PaymentGateway.ATTEMPTS_ALLOWED_PER_WOBBLE + 1) + "th is not");
        System.out.println("  declined — it is refused, and so is every one after it.");
        System.out.println();

        gateway.beginWobble();
        runIncident(List.of(billing, checkout, refunds, payouts));

        System.out.println();
        System.out.println("  What the gateway counted, from its own end:");
        printAttemptCounts(gateway.callLog());
        System.out.println();
        System.out.println("  Subscription billing spent half the shop's allowance before");
        System.out.println("  checkout had finished its first payment — and subscription");
        System.out.println("  billing succeeded. The sellers did not get paid, and there is");
        System.out.println("  nothing wrong with the payouts service. The code that");
        System.out.println("  misbehaved and the code that suffered are in different");
        System.out.println("  repositories, owned by different people, in different rooms.");
    }

    /** Take the four concerns out of the services and stand them beside them. */
    private static void actFour() {
        heading("Act 4 — move it out of the service and stand it next door");
        System.out.println("  Instead of each service knowing how to talk to the provider,");
        System.out.println("  each service talks to a proxy running beside it — same machine,");
        System.out.println("  same address, its own process. The service sends its payment to");
        System.out.println("  localhost. The proxy is the thing that goes out to the internet,");
        System.out.println("  and the proxy is where retrying, giving up, presenting the");
        System.out.println("  certificate and counting what happened all live now.");
        System.out.println();
        System.out.println("  All four proxies read the same configuration:");
        System.out.println("    " + SidecarConfig.agreedWithTheProvider().line());
        System.out.println();
        System.out.println("  And the service that used to carry twenty lines of retry code");
        System.out.println("  now carries one:");
        System.out.println();
        System.out.println("    public Receipt pay(Payment payment) {");
        System.out.println("        return sidecar.send(payment);");
        System.out.println("    }");
        System.out.println();

        PaymentGateway gateway = new PaymentGateway();
        gateway.beginWobble();
        System.out.println("  The same wobble, the same four payments, the same night:");
        System.out.println();
        runIncident(behindSidecars(gateway));
        System.out.println();
        System.out.println("  What the gateway counted:");
        printAttemptCounts(gateway.callLog());
        System.out.println();
        System.out.println("  Four payments, twelve attempts, nobody refused. The policy was");
        System.out.println("  not applied four times and missed once. It was stated once.");
    }

    /** What actually changed, counted both ways — including the way that got worse. */
    private static void actFive() {
        heading("Act 5 — what the pattern moved, and what it did not");
        System.out.printf("  %-38s %9s %9s%n", "", "before", "after");
        System.out.printf("  %-38s %9d %9d%n", "copies of a cross-cutting decision",
                Concerns.copiesInsideTheServices(4), Concerns.copiesBesideTheServices());
        System.out.printf("  %-38s %9d %9d%n", "places to edit for one policy change",
                Concerns.placesToEditAPolicy(4), Concerns.placesToEditAPolicyWithSidecars());
        System.out.printf("  %-38s %9d %9d%n", "processes to run and patch",
                Concerns.processesToRun(4, false), Concerns.processesToRun(4, true));
        System.out.println();
        System.out.println("  Read all three rows or none of them. The first two are why you");
        System.out.println("  would do this. The third is why it is not free: four proxies is");
        System.out.println("  four more things wanting memory, a version number, a restart");
        System.out.println("  when they are patched, and a line in somebody's runbook.");
        System.out.println();
        System.out.println("  The first row is the one that scales. Add a fifth service that");
        System.out.println("  takes payments and the copies go from "
                + Concerns.copiesInsideTheServices(4) + " to "
                + Concerns.copiesInsideTheServices(5) + " the old way;");
        System.out.println("  beside the services it is still " + Concerns.copiesBesideTheServices()
                + ". That method takes no");
        System.out.println("  argument at all, and the missing argument is the whole answer.");
        System.out.println();
        System.out.println("  The line for what may move out here: retry counts, deadlines,");
        System.out.println("  certificates and counters are facts about the network. Whether");
        System.out.println("  a refund is allowed after ninety days is a fact about the shop,");
        System.out.println("  and if it ever appears in a proxy configuration you have hidden");
        System.out.println("  a business rule somewhere no developer will think to look.");
    }

    /** You made calls more reliable by adding a dependency to every call. */
    private static void actSix() {
        heading("Act 6 — the second thing that can be down");
        PaymentGateway gateway = new PaymentGateway();
        gateway.behave();
        Sidecar sidecar = new Sidecar(CheckoutService.NAME, gateway,
                SidecarConfig.agreedWithTheProvider());
        ServiceBehindASidecar checkout = new ServiceBehindASidecar(CheckoutService.NAME, sidecar);

        System.out.println("  A healthy gateway, a healthy service, a "
                + Money.format(CHECKOUT.amountPence()) + " coffee maker:");
        Receipt receipt = checkout.pay(CHECKOUT);
        System.out.println("    " + receipt.describe());
        System.out.println();
        System.out.println("  Now the proxy beside checkout fails to start after a patch.");
        System.out.println("  The gateway is fine. The service is fine. The network is fine.");
        sidecar.stop();
        int attemptsBefore = gateway.callLog().total();
        try {
            checkout.pay(Payment.of("ORD-4418", 4799));
            System.out.println("    (it went through)");
        } catch (PaymentFailed failed) {
            System.out.println("    " + failed.getMessage());
        }
        System.out.println();
        System.out.println("  attempts that reached the gateway: "
                + (gateway.callLog().total() - attemptsBefore));
        System.out.println();
        System.out.println("  Zero. The request never left the machine, and the service has");
        System.out.println("  no retry code left to fall back on — we deleted it, on purpose,");
        System.out.println("  in Act 4. You added a dependency to every single call in order");
        System.out.println("  to make those calls more reliable. That trade is usually worth");
        System.out.println("  it, because a proxy on the same machine with no business logic");
        System.out.println("  in it fails far less often than the internet does. But it is a");
        System.out.println("  trade, and on the night it goes wrong it goes wrong for every");
        System.out.println("  call the service makes rather than for one of them.");
    }

    /** The hop you pay for ever, and the honest admission about what this is. */
    private static void actSeven() {
        heading("Act 7 — one millisecond, and what this pattern really is");
        PaymentGateway straight = new PaymentGateway();
        straight.beginWobble();
        straight.stopEnforcingQuota();
        CheckoutService inProcess = new CheckoutService(straight);
        inProcess.applyPolicyReview();
        Receipt without = inProcess.pay(CHECKOUT);

        PaymentGateway viaProxy = new PaymentGateway();
        viaProxy.beginWobble();
        viaProxy.stopEnforcingQuota();
        Sidecar sidecar = new Sidecar(CheckoutService.NAME, viaProxy,
                SidecarConfig.agreedWithTheProvider());
        Receipt with = sidecar.send(CHECKOUT);

        System.out.println("  The same payment, the same policy, the same wobble:");
        System.out.println();
        System.out.printf("    %-34s %d attempts, %dms%n", "retry code inside the service",
                without.attempts(), without.waitedMillis());
        System.out.printf("    %-34s %d attempts, %dms%n", "retry code in a proxy next door",
                with.attempts(), with.waitedMillis());
        System.out.println();
        System.out.println("  " + (with.waitedMillis() - without.waitedMillis())
                + " milliseconds, which is " + Sidecar.HOP_MILLIS + "ms per attempt for crossing to a");
        System.out.println("  neighbouring process and back. It is small, it is real, and it");
        System.out.println("  is paid on every call for as long as the service exists.");
        System.out.println();
        System.out.println("  And now the admission this project owes you. Everything you");
        System.out.println("  have watched happened inside one Java program. In one program,");
        System.out.println("  a proxy that a service talks through is an object wrapping");
        System.out.println("  another object — and an object wrapping another object is the");
        System.out.println("  Decorator pattern, from earlier in this course. The code is");
        System.out.println("  not new. The Sidecar class would not surprise anybody who has");
        System.out.println("  read Decorator.");
        System.out.println();
        System.out.println("  What makes this a different pattern is not the code. It is");
        System.out.println("  where the code runs. A decorator is compiled into your jar, is");
        System.out.println("  written in your language, and changes when your service is");
        System.out.println("  rebuilt. A sidecar is its own process, may be written in a");
        System.out.println("  language nobody on your team knows, and changes when somebody");
        System.out.println("  restarts it. That is what buys you the one-line policy change");
        System.out.println("  in Act 4, and it is what charges you the extra process in Act 5");
        System.out.println("  and the extra failure in Act 6.");
        System.out.println();
        System.out.println("  So the question is never 'wrapper or no wrapper'. It is: does");
        System.out.println("  this concern need to change without rebuilding the service, or");
        System.out.println("  apply to a service written in a language your library does not");
        System.out.println("  support? Yes to either, and it goes next door. No to both, and");
        System.out.println("  a shared library in your own process is cheaper and simpler.");
    }

    // --- helpers -----------------------------------------------------------------

    /** Runs the four payments in the order the night actually produced them. */
    private static void runIncident(List<? extends TakesPayments> services) {
        List<Payment> payments = List.of(SUBSCRIPTION, CHECKOUT, REFUND, PAYOUT);
        for (int i = 0; i < services.size(); i++) {
            TakesPayments service = services.get(i);
            Payment payment = payments.get(i);
            try {
                Receipt receipt = service.pay(payment);
                String effort = receipt.attempts() + "x, " + receipt.waitedMillis() + "ms";
                System.out.printf("    %-21s %-8s %-12s %s%n",
                        service.name(), Money.format(payment.amountPence()),
                        effort, receipt.providerRef());
            } catch (PaymentFailed failed) {
                System.out.printf("    %-21s %-8s %-12s %s%n",
                        service.name(), Money.format(payment.amountPence()), "—", "NOT PAID");
                System.out.println("      " + failed.getMessage());
            }
        }
    }

    private static List<TakesPayments> behindSidecars(PaymentGateway gateway) {
        SidecarConfig one = SidecarConfig.agreedWithTheProvider();
        return List.of(
                new ServiceBehindASidecar(SubscriptionBillingService.NAME,
                        new Sidecar(SubscriptionBillingService.NAME, gateway, one)),
                new ServiceBehindASidecar(CheckoutService.NAME,
                        new Sidecar(CheckoutService.NAME, gateway, one)),
                new ServiceBehindASidecar(RefundsService.NAME,
                        new Sidecar(RefundsService.NAME, gateway, one)),
                new ServiceBehindASidecar(MarketplacePayoutsService.NAME,
                        new Sidecar(MarketplacePayoutsService.NAME, gateway, one)));
    }

    private static void printGridHeader() {
        System.out.printf("    %-21s %8s %8s %9s %7s%n",
                "service", "attempts", "backoff", "deadline", "tls");
    }

    private static void printGrid(PaymentGateway gateway) {
        printGridHeader();
        printSettingsRow("checkout", new CheckoutService(gateway).settings());
        printSettingsRow("refunds", new RefundsService(gateway).settings());
        printSettingsRow("subscription-billing", new SubscriptionBillingService(gateway).settings());
        printSettingsRow("marketplace-payouts", new MarketplacePayoutsService(gateway).settings());
    }

    private static void printSettingsRow(String name, Settings settings) {
        System.out.printf("    %-21s %8d %8s %9s %7s%n",
                name,
                settings.maxAttempts(),
                settings.firstBackoffMillis() + "ms",
                settings.deadlineMillis() + "ms",
                settings.tlsProfile());
    }

    private static void printAttemptCounts(CallLog log) {
        for (Map.Entry<String, Integer> entry : log.byService().entrySet()) {
            int count = entry.getValue();
            System.out.printf("    %-21s %d attempt%s%n",
                    entry.getKey(), count, count == 1 ? "" : "s");
        }
        System.out.printf("    %-21s %d of %d allowed, %d refused%n",
                "total", log.total(), PaymentGateway.ATTEMPTS_ALLOWED_PER_WOBBLE,
                log.countOf("rate-limited"));
    }

    private static void heading(String title) {
        System.out.println();
        System.out.println("=".repeat(72));
        System.out.println(title);
        System.out.println("=".repeat(72));
    }

    private PaymentsDemo() {
    }
}
