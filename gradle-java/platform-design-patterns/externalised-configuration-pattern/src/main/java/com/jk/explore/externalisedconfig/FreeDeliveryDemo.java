package com.jk.explore.externalisedconfig;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Nine acts. A threshold that only a software release can change, a weekend
 * promotion that misses the weekend, the same threshold read from outside the
 * program — and then the bill, which is three acts long and is the part most
 * write-ups leave out.
 *
 * <p>The story is one line of code: free delivery when you spend over fifty
 * pounds. Marketing wants thirty-five for one weekend, starting nine o'clock on
 * Saturday morning, and they ask on Friday afternoon.
 */
public final class FreeDeliveryDemo {

    /** Marketing asks late on a Friday afternoon. This is the whole problem. */
    private static final LocalDateTime FRIDAY_AFTERNOON =
            LocalDateTime.of(2025, 3, 7, 16, 30);

    /** When the promotion was supposed to start. */
    private static final LocalDateTime SATURDAY_MORNING =
            LocalDateTime.of(2025, 3, 8, 9, 0);

    private static final LocalDateTime SATURDAY_0912 = LocalDateTime.of(2025, 3, 8, 9, 12);
    private static final LocalDateTime SATURDAY_0920 = LocalDateTime.of(2025, 3, 8, 9, 20);
    private static final LocalDateTime SATURDAY_1005 = LocalDateTime.of(2025, 3, 8, 10, 5);
    private static final LocalDateTime SATURDAY_1140 = LocalDateTime.of(2025, 3, 8, 11, 40);

    private static final String KEY = ConfiguredCheckout.FREE_DELIVERY_OVER.key();

    /** Three baskets that between them straddle both thresholds. */
    private static final List<Basket> BASKETS = List.of(
            new Basket("ORD-7101", Money.pounds(62)),
            new Basket("ORD-7102", Money.pounds(48)),
            new Basket("ORD-7103", Money.pence(3150)));

    // Acts 3 to 9 share one server and one log, so the audit trail in act 8 is
    // the real history of everything the earlier acts did. They are instance
    // fields rather than statics so that running the demo twice — which the test
    // suite does, to prove the output is identical every time — starts from the
    // same empty log on both runs.
    private final ChangeLog log = new ChangeLog();
    private final ConfigServer server = new ConfigServer(FRIDAY_AFTERNOON, log);

    public static void main(String[] args) {
        new FreeDeliveryDemo().run();
    }

    /** All nine acts, in order. */
    public void run() {
        theThresholdInTheCode();
        whatChangingItActuallyCosts();
        theSameThresholdReadFromOutside();
        theSourceIsUnreachable();
        theBillABadNumberNobodyNotices();
        theBillAValueThatIsNotANumber();
        theMitigationTypedAndValidated();
        theMitigationAnAuditTrail();
        theMitigationRollbackAsFastAsTheChange();
    }

    /** Act 1: the shop as it stands, quoting correctly on a compiled-in number. */
    private void theThresholdInTheCode() {
        System.out.println("Act 1 - free delivery over " + HardCodedCheckout.threshold()
                + ", and the number lives in the source");

        Checkout checkout = new HardCodedCheckout();
        for (Basket basket : BASKETS) {
            System.out.println("    " + checkout.quote(basket).asLine());
        }
        System.out.println("  nothing here is wrong. It is a named constant, in one place,"
                + " and a reviewer would pass it.");
        System.out.println("  the threshold came from: "
                + checkout.quote(BASKETS.get(0)).thresholdCameFrom());
        System.out.println();
    }

    /** Act 2: marketing asks for £35 from Saturday, and the pipeline answers. */
    private void whatChangingItActuallyCosts() {
        System.out.println("Act 2 - marketing wants " + Money.pounds(35)
                + " from " + ReleasePipeline.inWords(SATURDAY_MORNING) + ", and asks on"
                + " Friday at 16:30");

        ReleasePipeline pipeline = ReleasePipeline.typical();
        for (ReleasePipeline.ScheduledStep step : pipeline.schedule(FRIDAY_AFTERNOON)) {
            System.out.println(step.asLine());
        }
        LocalDateTime live = pipeline.liveAt(FRIDAY_AFTERNOON);
        Duration late = pipeline.lateBy(SATURDAY_MORNING, FRIDAY_AFTERNOON);
        System.out.println("  total work: "
                + ReleasePipeline.inWords(pipeline.totalWork()));
        System.out.println("  live at:    " + ReleasePipeline.inWords(live));
        System.out.println("  the promotion was for the weekend. It is late by "
                + ReleasePipeline.inWords(late) + ".");
        System.out.println("  no step in that list is unreasonable. A deploy is simply not"
                + " a thing you do at 9am on a Saturday.");
        System.out.println();
    }

    /** Act 3: the number moves outside the program, and the change lands in seconds. */
    private void theSameThresholdReadFromOutside() {
        System.out.println("Act 3 - the same threshold, read from a configuration source"
                + " on every quote");

        Checkout checkout = new ConfiguredCheckout(new TrustingSettings(server));
        System.out.println("  before the change, with nothing configured:");
        for (Basket basket : BASKETS) {
            System.out.println("    " + checkout.quote(basket).asLine());
        }

        ConfigChange change = server.set(KEY, "35", "marketing");
        System.out.println("  " + change.asLine());
        System.out.println("  the very next quote, " + ConfigServer.WRITE_TAKES.toSeconds()
                + " seconds later:");
        for (Basket basket : BASKETS) {
            System.out.println("    " + checkout.quote(basket).asLine());
        }
        System.out.println("  ORD-7102 now ships free. No rebuild, no redeploy, no"
                + " restart.");
        System.out.println("  the threshold came from: "
                + checkout.quote(BASKETS.get(0)).thresholdCameFrom());
        System.out.println();
    }

    /** Act 4: the config server goes away and the shop keeps selling. */
    private void theSourceIsUnreachable() {
        System.out.println("Act 4 - the config server stops answering");

        Checkout checkout = new ConfiguredCheckout(new TrustingSettings(server));
        server.goOffline("the network link to it dropped");
        DeliveryQuote quote = checkout.quote(BASKETS.get(1));
        System.out.println("    " + quote.asLine());
        System.out.println("  threshold in force: " + quote.thresholdApplied());
        System.out.println("  came from: " + quote.thresholdCameFrom());
        System.out.println("  the shop starts and keeps selling, because the code carries"
                + " its own default.");
        System.out.println("  note what it quietly lost, though: the promotion. Back to "
                + Money.pounds(50) + " with no error and no alarm.");
        server.comeBackOnline();
        System.out.println();
    }

    /** Act 5: the first half of the bill. A well-formed, catastrophic number. */
    private void theBillABadNumberNobodyNotices() {
        System.out.println("Act 5 - the bill: somebody types -1 into the box on Saturday"
                + " morning");

        server.fastForwardTo(SATURDAY_0912);
        ConfigChange change = server.set(KEY, "-1", "marketing");
        System.out.println("  " + change.asLine());

        Checkout checkout = new ConfiguredCheckout(new TrustingSettings(server));
        for (Basket basket : BASKETS) {
            System.out.println("    " + checkout.quote(basket).asLine());
        }
        System.out.println("  every basket in the shop now ships free, including the"
                + " " + BASKETS.get(2).goodsTotal() + " one.");
        System.out.println("  -1 is a perfectly well-formed number, so nothing complains."
                + " There is no exception and no log line.");
        System.out.println("  it reached the running shop in "
                + ConfigServer.WRITE_TAKES.toSeconds() + " seconds, with no compiler, no"
                + " code review and no test suite in the way.");
        System.out.println("  that is what you traded the release pipeline for.");
        System.out.println();
    }

    /** Act 6: the second half of the bill. Text that is not a number at all. */
    private void theBillAValueThatIsNotANumber() {
        System.out.println("Act 6 - the bill: eight minutes later, somebody types the word"
                + " fifty");

        server.fastForwardTo(SATURDAY_0920);
        ConfigChange change = server.set(KEY, "fifty", "marketing");
        System.out.println("  " + change.asLine());

        Checkout checkout = new ConfiguredCheckout(new TrustingSettings(server));
        for (Basket basket : BASKETS) {
            try {
                checkout.quote(basket);
                System.out.println("    " + basket.orderId()
                        + "  quoted without complaint, which would be worse");
            } catch (InvalidSettingException failed) {
                System.out.println("    " + basket.orderId() + "  checkout failed: "
                        + failed.getMessage());
            }
        }
        System.out.println("  not one basket can be quoted. The shop is down, and it was"
                + " taken down by a text box.");
        System.out.println("  the config server stored it happily, because storing text is"
                + " all a config server does.");
        System.out.println();
    }

    /** Act 7: the mitigation that replaces the compiler — a typed, ranged setting. */
    private void theMitigationTypedAndValidated() {
        System.out.println("Act 7 - the mitigation: declare the setting, and validate at"
                + " the boundary");

        MoneySetting setting = ConfiguredCheckout.FREE_DELIVERY_OVER;
        System.out.println("  " + setting.key() + ": money, "
                + setting.describeRange() + ", default " + setting.fallback());

        GuardedSettings guarded = new GuardedSettings(server);
        Checkout checkout = new ConfiguredCheckout(guarded);

        System.out.println("  the word fifty is still configured. With validation on:");
        DeliveryQuote first = checkout.quote(BASKETS.get(0));
        System.out.println("    " + first.asLine() + "   threshold "
                + first.thresholdApplied());
        System.out.println("    came from: " + first.thresholdCameFrom());

        server.fastForwardTo(SATURDAY_1005);
        System.out.println("  " + server.set(KEY, "35", "marketing").asLine());
        DeliveryQuote good = checkout.quote(BASKETS.get(1));
        System.out.println("    " + good.asLine() + "   threshold "
                + good.thresholdApplied() + ", from " + good.thresholdCameFrom());

        server.fastForwardTo(SATURDAY_1140);
        System.out.println("  " + server.set(KEY, "-1", "ops").asLine());
        DeliveryQuote afterBadValue = checkout.quote(BASKETS.get(2));
        System.out.println("    " + afterBadValue.asLine() + "   threshold "
                + afterBadValue.thresholdApplied());
        System.out.println("    came from: " + afterBadValue.thresholdCameFrom());

        for (String rejection : guarded.rejections()) {
            System.out.println("  " + rejection);
        }
        System.out.println("  both bad values were stopped at the edge, and the shop kept"
                + " the last value that passed.");
        System.out.println("  it did not revert to " + setting.fallback()
                + " either, because throwing away a good promotion over an unrelated typo"
                + " is its own kind of wrong.");
        System.out.println();
    }

    /** Act 8: the mitigation that replaces the version history. */
    private void theMitigationAnAuditTrail() {
        System.out.println("Act 8 - the mitigation: who changed what, and when");

        for (ConfigChange change : log.changesTo(KEY)) {
            System.out.println("  " + change.asLine());
        }
        System.out.println("  " + log.size() + " changes to one setting in under a day, and"
                + " not one of them is in the git history.");
        System.out.println("  when the value left the source code it left the version"
                + " control behind. This list is the replacement.");
        System.out.println("  the question you will be asked is never what the threshold is"
                + " now. It is what it was at 9am on Saturday.");
        System.out.println();
    }

    /** Act 9: the mitigation that only externalised configuration can offer. */
    private void theMitigationRollbackAsFastAsTheChange() {
        System.out.println("Act 9 - the mitigation: a rollback as fast as the change");

        LocalDateTime noticedAt = server.now();
        ConfigChange rollback = server.rollback(KEY, "on-call").orElseThrow();
        System.out.println("  " + rollback.asLine());
        System.out.println("  back in force at " + ConfigServer.WRITE_TAKES.toSeconds()
                + " seconds past the decision, and nobody had to remember the old value:"
                + " the log had it.");

        ReleasePipeline pipeline = ReleasePipeline.typical();
        System.out.println("  the same correction through the release pipeline would be"
                + " live " + ReleasePipeline.inWords(pipeline.liveAt(noticedAt)) + ".");

        Checkout checkout = new ConfiguredCheckout(new GuardedSettings(server));
        for (Basket basket : BASKETS) {
            System.out.println("    " + checkout.quote(basket).asLine());
        }
        System.out.println("  externalised configuration is not a way to avoid governing a"
                + " change. It is a way to govern it in seconds instead of days.");
        System.out.println("  take the number out of the code, and take the compiler, the"
                + " reviewer and the history with it - as validation, a schema, an audit"
                + " trail and a rollback.");
        System.out.println();
    }
}
