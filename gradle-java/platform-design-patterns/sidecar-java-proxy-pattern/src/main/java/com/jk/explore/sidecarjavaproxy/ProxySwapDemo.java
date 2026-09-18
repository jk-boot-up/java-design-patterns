package com.jk.explore.sidecarjavaproxy;

import java.util.List;

/**
 * One job, in seven acts: change the proxy under a service that never restarts.
 *
 * <p>The structure of this file is part of the argument, so it is worth saying out loud
 * before you read it. There is exactly one {@code new PaymentsService(...)} in the whole
 * program, in {@link #main}, and every act below is handed that same instance. The demo
 * could not restart the service between acts even if it wanted to, because there is
 * nowhere left to do it. What changes, twice, is what is bound to the port next door.
 *
 * <p>Acts 1 to 3 are the gap §41 shipped with: nginx retries three times and does not
 * wait, so a payment during a wobble fails having spent the whole allowance in three
 * milliseconds. Acts 4 and 5 are the swap and what it buys. Acts 6 and 7 are what it
 * costs, because a pattern taught without its costs is an advertisement.
 *
 * <p>Every number printed below is measured. Attempt times come from the provider's own
 * log rather than from the proxy that made them, and the clock is moved by hand so the
 * figures are identical on every machine.
 */
public final class ProxySwapDemo {

    private static final Payment HEALTHY = Payment.of("ORD-4417", 4799);
    private static final Payment DURING_WOBBLE = Payment.of("ORD-4418", 4799);
    private static final Payment MID_SWAP = Payment.of("ORD-4419", 3150);
    private static final Payment AFTER_SWAP = Payment.of("ORD-4420", 4799);

    public static void main(String[] args) {
        PaymentsService.nothingIsRunningYet();
        PaymentGateway provider = new PaymentGateway();
        ProxyPolicy policy = ProxyPolicy.agreedWithTheProvider();
        NginxProxy nginx = new NginxProxy(PaymentsService.NAME, provider, policy);
        JavaProxy java = new JavaProxy(PaymentsService.NAME, provider, policy);
        LocalPort port = new LocalPort(nginx);

        // The only one in the program. Everything after this line reuses it.
        PaymentsService checkout = new PaymentsService(PaymentsService.NAME, port);

        actOne(checkout, provider);
        actTwo(checkout, provider);
        actThree(policy);
        actFour(checkout, port, java, provider);
        actFive(checkout, provider);
        actSix(checkout, port, nginx, java, provider);
        actSeven(nginx, java);
    }

    /** Where §41 left us: a service with nothing in it, and a proxy that works. */
    private static void actOne(PaymentsService checkout, PaymentGateway provider) {
        heading("Act 1 — where the last project left off");
        System.out.println("  Checkout takes payments, and the code that knows how to talk to");
        System.out.println("  the payment provider is not in it any more. It was moved next");
        System.out.println("  door into a proxy, which is what the Sidecar pattern is, and");
        System.out.println("  that project is the one to read first. This project has one job");
        System.out.println("  and it is not explaining sidecars.");
        System.out.println();
        System.out.println("  The service's entire configuration for reaching the provider:");
        System.out.println("    " + checkout.configuredEndpoint());
        System.out.println();
        System.out.println("  An address on its own machine. Not a provider hostname, not a");
        System.out.println("  certificate, not a retry count. Whatever is listening there");
        System.out.println("  answers, and checkout has no way to find out what it is.");
        System.out.println();
        System.out.println("  Today it is " + checkout.port().occupant().name()
                + ", written in " + checkout.port().occupant().language() + ",");
        System.out.println("  about " + checkout.port().occupant().lines()
                + " lines, maintained by people the shop has never met.");
        System.out.println();

        provider.behave();
        Receipt receipt = checkout.pay(HEALTHY);
        System.out.println("  A healthy " + Money.format(HEALTHY.amountPence()) + " coffee maker:");
        System.out.println("    " + receipt.describe());
    }

    /** The wobble, and the three attempts that all land in the same millisecond window. */
    private static void actTwo(PaymentsService checkout, PaymentGateway provider) {
        heading("Act 2 — the wobble, and three attempts that bought nothing");
        System.out.println("  The provider has a bad " + PaymentGateway.RECOVERS_AT_MILLIS
                + " milliseconds. Nothing is broken");
        System.out.println("  and nobody needs paging: it declines everything, and then it");
        System.out.println("  is fine. In March it wrote to every merchant asking for two");
        System.out.println("  things — at most three attempts per payment, and wait properly");
        System.out.println("  between them. The shop agreed to both.");
        System.out.println();

        provider.beginWobble();
        System.out.println("  Checkout asks for " + Money.format(DURING_WOBBLE.amountPence()) + ":");
        attempt(checkout, DURING_WOBBLE);
        System.out.println();
        System.out.println("  What the provider itself recorded:");
        printAttempts(provider.callLog());
        System.out.println();
        System.out.println("  Three attempts, spanning " + provider.callLog().spanMillis()
                + " milliseconds, and the provider");
        System.out.println("  did not recover until " + PaymentGateway.RECOVERS_AT_MILLIS
                + ". Every one of them landed inside the");
        System.out.println("  bad window, because they were all made inside the bad window.");
        System.out.println("  The shop spent its whole allowance for this payment before the");
        System.out.println("  provider had time to get better, and the customer got nothing.");
        System.out.println();
        System.out.println("  The half of the agreement that limits the shop was kept. The");
        System.out.println("  half that would have helped was not.");
    }

    /** Why the configuration cannot be fixed: there is no directive for it. */
    private static void actThree(ProxyPolicy policy) {
        heading("Act 3 — the line of configuration that does not exist");
        System.out.println("  The obvious response is to go and fix the proxy's configuration.");
        System.out.println("  There is nothing to fix it with.");
        System.out.println();
        System.out.println("  nginx retries by moving to the next server in its upstream group,");
        System.out.println("  which is why the configuration lists the provider's address three");
        System.out.println("  times to mean three attempts. Moving to the next server happens");
        System.out.println("  immediately. That was a good decision for the case it was built");
        System.out.println("  for — a pool of machines, where the next machine is a different");
        System.out.println("  machine and is probably fine. Here every entry in the pool is the");
        System.out.println("  one address that is currently unwell.");
        System.out.println();
        System.out.println("  The policy everybody agreed to:");
        System.out.println("    " + policy.line());
        System.out.println();
        System.out.println("  What the installed proxy has no words for:");
        for (String gap : new NginxProxy(PaymentsService.NAME, new PaymentGateway(), policy)
                .cannotExpress()) {
            System.out.println("    " + gap);
        }
        System.out.println();
        System.out.println("  Three ways out, and it is worth seeing why two of them are bad:");
        System.out.println();
        System.out.println("    put the waiting back in the service   undoes the last project");
        System.out.println("    script the proxy in Lua or njs        now you are writing code");
        System.out.println("                                          anyway, in a language you");
        System.out.println("                                          chose for its config file");
        System.out.println("    put a different proxy on the port     — this project");
        System.out.println();
        System.out.println("  The third one is only available because of a decision made in the");
        System.out.println("  last project: the contract between the service and the proxy is");
        System.out.println("  an address, not a library. Nothing about it is Java, or nginx.");
    }

    /** The swap itself, with the evidence that the service was not touched. */
    private static void actFour(PaymentsService checkout, LocalPort port,
                                JavaProxy java, PaymentGateway provider) {
        heading("Act 4 — the swap");
        System.out.println("  Somebody writes a proxy. It is about " + java.lines()
                + " lines of Java: read");
        System.out.println("  the policy, try, catch, wait, double the wait, try again. It");
        System.out.println("  goes on the same port, beside the same service, and it is handed");
        System.out.println("  the very same policy object the nginx proxy was reading.");
        System.out.println();
        System.out.printf("  %-34s %s%n", "before the swap, listening on "
                + port.address() + ":", port.occupant().name());
        System.out.printf("  %-34s %s%n", "checkout is on start number:",
                checkout.startNumber());
        System.out.printf("  %-34s %s%n", "checkout's configured endpoint:",
                checkout.configuredEndpoint());
        System.out.println();

        port.install(java);

        System.out.printf("  %-34s %s%n", "after the swap, listening:", port.occupant().name());
        System.out.printf("  %-34s %s%n", "checkout is on start number:",
                checkout.startNumber());
        System.out.printf("  %-34s %s%n", "checkout's configured endpoint:",
                checkout.configuredEndpoint());
        System.out.printf("  %-34s %s%n", "payments services ever started:",
                PaymentsService.startsSoFar());
        System.out.println();
        System.out.println("  One line changed and it was not in the service. The start number");
        System.out.println("  did not move, and that is not the demo being careful: there is");
        System.out.println("  exactly one place in this whole program where a payments service");
        System.out.println("  is constructed, and it runs before Act 1.");
        System.out.println();
        System.out.println("  Checkout was not told. There is no method on it to tell.");
        System.out.println();

        provider.behave();
        Receipt receipt = checkout.pay(AFTER_SWAP);
        System.out.println("  The same call it has always made, through a neighbour that has");
        System.out.println("  changed language since the last one:");
        System.out.println("    " + receipt.describe());
    }

    /** The same wobble, the same three attempts, spread out. */
    private static void actFive(PaymentsService checkout, PaymentGateway provider) {
        heading("Act 5 — the same wobble, the same three attempts");
        provider.beginWobble();
        System.out.println("  Identical provider, identical bad "
                + PaymentGateway.RECOVERS_AT_MILLIS + " milliseconds, identical");
        System.out.println("  payment, identical allowance of three attempts:");
        System.out.println();
        attempt(checkout, DURING_WOBBLE);
        System.out.println();
        System.out.println("  What the provider itself recorded:");
        printAttempts(provider.callLog());
        System.out.println();
        System.out.println("  Still three attempts. The shop is not being greedier and the");
        System.out.println("  provider's allowance is untouched — the third attempt simply");
        System.out.println("  arrives " + provider.callLog().spanMillis()
                + " milliseconds after the first, rather than 2,");
        System.out.println("  and by then the provider is well again.");
        System.out.println();
        System.out.println("  Nothing about the provider changed between Act 2 and this one.");
        System.out.println("  Nothing about the service changed either. The spacing changed,");
        System.out.println("  and the spacing was the difference between a customer walking");
        System.out.println("  away and a coffee maker being sold.");
    }

    /** The swap window, and the fact that the port really is empty for a moment. */
    private static void actSix(PaymentsService checkout, LocalPort port,
                               NginxProxy nginx, JavaProxy java, PaymentGateway provider) {
        heading("Act 6 — the gap in the middle of a swap");
        System.out.println("  Acts 4 and 5 skipped something, and it is the thing that will");
        System.out.println("  actually page somebody. A swap is not instant. The old proxy");
        System.out.println("  stops, and for a moment there is nothing on the port at all.");
        System.out.println();

        provider.behave();
        port.vacate();
        System.out.println("  The provider is healthy. The network is healthy. Checkout is");
        System.out.println("  healthy. A customer pays for a "
                + Money.format(MID_SWAP.amountPence()) + " kettle:");
        int before = provider.callLog().total();
        attempt(checkout, MID_SWAP);
        System.out.println();
        System.out.println("  attempts that reached the provider: "
                + (provider.callLog().total() - before));
        System.out.println();
        System.out.println("  Zero, and there is nothing to fall back on. The retry code that");
        System.out.println("  would have covered this was deleted in the last project, and");
        System.out.println("  deleting it was the right call — but it means the swap window is");
        System.out.println("  a window of hard failures rather than slow ones.");
        System.out.println();

        port.install(java);
        System.out.println("  Bringing the new proxy up is the whole repair:");
        System.out.println("    " + checkout.pay(Payment.of("ORD-4421", 3150)).describe());
        System.out.println();
        System.out.println("  So a real swap is not one line in a demo; it is a rollout. Start");
        System.out.println("  the new proxy before stopping the old one, move one service at a");
        System.out.println("  time, and keep the old proxy installable — because the honest");
        System.out.println("  reason to be able to swap forwards is to be able to swap back.");
        System.out.println();
        System.out.printf("  %-34s %s%n", "still listening:", port.occupant().name());
        System.out.printf("  %-34s %d%n", "times the port has been replaced:", port.swaps());
        System.out.printf("  %-34s %d%n", "times the service has restarted:",
                checkout.startNumber() - 1);
        System.out.println();
        System.out.println("  And the proxy that is no longer installed still exists, still");
        System.out.println("  works, and would go back on the port in one line: "
                + nginx.name() + ",");
        System.out.println("  " + nginx.lines() + " lines, against " + java.lines()
                + " for the one that replaced it.");
    }

    /** What forty lines of your own really cost. */
    private static void actSeven(NginxProxy nginx, JavaProxy java) {
        heading("Act 7 — what you just bought, and what you paid for it");
        System.out.printf("  %-12s %-21s %5s%n", "proxy", "language", "lines");
        for (Proxy proxy : List.of(nginx, java)) {
            System.out.printf("  %-12s %-21s %5d%n",
                    proxy.name(), proxy.language(), proxy.lines());
        }
        System.out.println();
        for (Proxy proxy : List.of(nginx, java)) {
            System.out.println("  what " + proxy.name() + " has no words for:");
            if (proxy.cannotExpress().isEmpty()) {
                System.out.println("    nothing");
            }
            for (String gap : proxy.cannotExpress()) {
                System.out.println("    " + gap);
            }
        }
        System.out.println();
        System.out.println("  That table is the demonstration this project exists for. The");
        System.out.println("  last project claimed a sidecar is language-independent. A claim");
        System.out.println("  is not a demonstration. Two proxies, two languages, one port,");
        System.out.println("  and a service whose source file is byte-for-byte the same in");
        System.out.println("  both runs — that is a demonstration.");
        System.out.println();
        System.out.println("  Now the bill, and it is longer than the benefit.");
        System.out.println();
        System.out.println("    " + nginx.lines() + " lines of somebody else's configuration became "
                + java.lines() + " lines");
        System.out.println("    of your own code. Yours to test, to review, to keep working");
        System.out.println("    on the next JDK, and to fix at three in the morning.");
        System.out.println();
        System.out.println("    Everything nginx brought for free and this file does not have:");
        System.out.println("    TLS termination, a structured access log, connection pooling,");
        System.out.println("    and twenty years of somebody answering security advisories");
        System.out.println("    before you have heard of them.");
        System.out.println();
        System.out.println("    A JVM beside every service, where a few megabytes of nginx");
        System.out.println("    used to sit. Multiply by the number of services.");
        System.out.println();
        System.out.println("    And nothing now stops the next person putting the shop's");
        System.out.println("    refund rules in the proxy, because it is a general-purpose");
        System.out.println("    language and it will happily let them.");
        System.out.println();
        System.out.println("  So the rule is narrow, and it is the only thing to take away:");
        System.out.println("  swap the proxy when the thing you need cannot be said in the");
        System.out.println("  configuration language at all. Not when it is awkward. Not when");
        System.out.println("  you would rather write Java. Here the missing sentence was the");
        System.out.println("  difference between a payment going through and a payment");
        System.out.println("  failing, and that clears the bar. Very little else does.");
        System.out.println();
        System.out.println("  The part worth keeping either way is that the choice was");
        System.out.println("  available. Because the service talks to an address, swapping the");
        System.out.println("  proxy was a decision somebody could make on a Tuesday afternoon,");
        System.out.println("  and swapping it back is the same decision in the other order.");
    }

    // --- helpers -----------------------------------------------------------------

    private static void attempt(PaymentsService service, Payment payment) {
        try {
            Receipt receipt = service.pay(payment);
            System.out.printf("    %-12s %-9s %s%n", payment.orderRef(),
                    Money.format(payment.amountPence()), receipt.describe());
        } catch (PaymentFailed failed) {
            System.out.printf("    %-12s %-9s %s%n", payment.orderRef(),
                    Money.format(payment.amountPence()), "NOT PAID");
            System.out.println("      " + failed.getMessage());
        }
    }

    private static void printAttempts(CallLog log) {
        for (CallLog.Attempt attempt : log.attempts()) {
            System.out.printf("    attempt at %4dms   %s%n", attempt.atMillis(),
                    attempt.outcome());
        }
        System.out.printf("    %d attempts, first to last: %dms%n",
                log.total(), log.spanMillis());
    }

    private static void heading(String title) {
        System.out.println();
        System.out.println("=".repeat(72));
        System.out.println(title);
        System.out.println("=".repeat(72));
    }

    private ProxySwapDemo() {
    }
}
