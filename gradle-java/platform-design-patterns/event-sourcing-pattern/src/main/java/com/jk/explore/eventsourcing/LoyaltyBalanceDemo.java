package com.jk.explore.eventsourcing;

import java.time.LocalDate;
import java.util.List;

/**
 * Nine acts. A question a row cannot answer, a bug that destroys its own evidence,
 * the log that answers all three questions instead, and then the bill.
 *
 * <p>The story is one customer, C-4417, whose loyalty balance says 140 points, and
 * a support agent who has been asked why.
 */
public final class LoyaltyBalanceDemo {

    // March 2025. Fixed dates rather than a clock, so every run prints the same
    // thing and the as-of query has a real calendar to work against.
    private static final LocalDate MAR_1 = LocalDate.of(2025, 3, 1);
    private static final LocalDate MAR_3 = LocalDate.of(2025, 3, 3);
    private static final LocalDate MAR_8 = LocalDate.of(2025, 3, 8);
    private static final LocalDate MAR_14 = LocalDate.of(2025, 3, 14);
    private static final LocalDate MAR_20 = LocalDate.of(2025, 3, 20);

    private static final String C = "C-4417";

    private LoyaltyBalanceDemo() {
    }

    public static void main(String[] args) {
        theQuestionTheRowCannotAnswer();
        theBugThatDestroysItsOwnEvidence();
        theSameBugWithALogBehindIt();
        whyItIs140();
        whatItWasOnTheThirdOfMarch();
        theBillTheLongStream();
        theBillTheErasureRequest();
        theBillTheEventYouCanNeverChange();
        eventSourcingIsNotCqrs();
    }

    /** Act 1: support asks why the balance is 140, and the row has one sentence. */
    private static void theQuestionTheRowCannotAnswer() {
        System.out.println("Act 1 - a customer asks why their balance is 140");

        CurrentStateLoyaltyAccounts accounts = new CurrentStateLoyaltyAccounts();
        marchForCustomer(accounts);

        System.out.println("  balance: " + accounts.balanceFor(C));
        System.out.println("  support asks why, and this is the whole answer:");
        System.out.println("    " + accounts.explain(C));
        System.out.println("  the four things that happened in March were each added to a"
                + " number and then forgotten.");
        System.out.println();
    }

    /** Act 2: the bug lands on the row, and takes the evidence with it. */
    private static void theBugThatDestroysItsOwnEvidence() {
        System.out.println("Act 2 - a release awards points twice, and nobody notices"
                + " for three weeks");

        CurrentStateLoyaltyAccounts accounts = new CurrentStateLoyaltyAccounts();
        Checkout checkout = new Checkout(accounts);

        // Before the bug: two of the three customers already had points.
        checkout.placeOrder("C-5120", "ORD-8990", 10, MAR_1);
        checkout.placeOrder("C-5122", "ORD-8991", 25, MAR_1);

        checkout.shipTheDoubleAwardingRelease();
        checkout.placeOrder("C-5120", "ORD-9001", 45, MAR_8);
        checkout.placeOrder("C-5121", "ORD-9002", 30, MAR_8);
        checkout.shipTheFix();

        System.out.println("  the fix is out. Now find the customers it touched:");
        for (String customer : accounts.customers()) {
            System.out.println("    " + customer + " = " + accounts.balanceFor(customer)
                    + " points");
        }
        System.out.println("  which of those three is wrong, and by how much?");
        System.out.println("  100 could be a doubled £45 order on top of £10, or one"
                + " honest £100 order. Both write 100.");
        System.out.println("  the information needed to tell them apart was overwritten"
                + " by the bug itself.");
        System.out.println();
    }

    /** Act 3: the same bug, over a log, is a query. */
    private static void theSameBugWithALogBehindIt() {
        System.out.println("Act 3 - the same bug, with an append-only log behind it");

        LoyaltyEventStore store = new LoyaltyEventStore();
        EventSourcedLoyaltyAccounts accounts = new EventSourcedLoyaltyAccounts(store);
        Checkout checkout = new Checkout(accounts);

        checkout.placeOrder("C-5120", "ORD-8990", 10, MAR_1);
        checkout.shipTheDoubleAwardingRelease();
        checkout.placeOrder("C-5120", "ORD-9001", 45, MAR_8);
        checkout.shipTheFix();

        System.out.println("  balance as the log stands: "
                + accounts.balanceFor("C-5120") + " points");
        System.out.println("  orders that earned points more than once:");
        for (String duplicate : accounts.duplicateAwards("C-5120")) {
            System.out.println("    " + duplicate);
        }
        System.out.println("  nobody wrote that query before the bug shipped. It was"
                + " written after, and the data was already there.");
        System.out.println("  balance with the second award ignored: "
                + accounts.balanceWithDuplicateAwardsIgnored("C-5120") + " points");
        System.out.println("  no event was edited and none was deleted. The reading code"
                + " changed, and every balance is right again.");
        System.out.println();
    }

    /** Act 4: the answer support actually needed. */
    private static void whyItIs140() {
        System.out.println("Act 4 - why it is 140");

        EventSourcedLoyaltyAccounts accounts = marchForCustomer(
                new EventSourcedLoyaltyAccounts(new LoyaltyEventStore()));

        System.out.println("  balance: " + accounts.balanceFor(C)
                + " points, and this time there is a reason:");
        for (String line : accounts.explain(C)) {
            System.out.println("    " + line);
        }
        System.out.println("  the balance is not stored anywhere. That number is the"
                + " four events added up, worked out just now.");
        System.out.println();
    }

    /** Act 5: a question nobody planned for. */
    private static void whatItWasOnTheThirdOfMarch() {
        System.out.println("Act 5 - and what was it on the third of March?");

        EventSourcedLoyaltyAccounts accounts = marchForCustomer(
                new EventSourcedLoyaltyAccounts(new LoyaltyEventStore()));

        System.out.println("  on 1 March:  " + accounts.balanceOn(C, MAR_1) + " points");
        System.out.println("  on 3 March:  " + accounts.balanceOn(C, MAR_3) + " points");
        System.out.println("  on 8 March:  " + accounts.balanceOn(C, MAR_8) + " points");
        System.out.println("  on 20 March: " + accounts.balanceOn(C, MAR_20) + " points");
        System.out.println("  nobody decided in advance to record any of those. It is the"
                + " same sum, stopped earlier.");
        System.out.println();
    }

    /** Act 6: the first part of the bill, in read counts. */
    private static void theBillTheLongStream() {
        System.out.println("Act 6 - the bill: a stream long enough to need a snapshot");

        LoyaltyEventStore store = new LoyaltyEventStore();
        EventSourcedLoyaltyAccounts plain = new EventSourcedLoyaltyAccounts(store);
        // Five years of a busy shop: twenty customers, two hundred and fifty
        // events each.
        for (int round = 0; round < 250; round++) {
            for (int customer = 0; customer < 20; customer++) {
                plain.award("C-6" + String.format("%03d", customer), 2,
                        "ORD-" + round + "-" + customer, MAR_1);
            }
        }
        System.out.println("  events in the log: " + store.size());

        store.resetMeter();
        int balance = plain.balanceFor("C-6000");
        System.out.println("  one balance, folded from the start: " + balance
                + " points, " + store.eventsExamined() + " events read");

        // The snapshot is taken here, at event 5,000, and then one more order
        // arrives. Both ways of answering are measured after that order, so the
        // two figures below are the same question asked twice.
        SnapshotStore snapshots = new SnapshotStore();
        EventSourcedLoyaltyAccounts snapshotted =
                new EventSourcedLoyaltyAccounts(store, snapshots);
        snapshots.save(snapshotted.snapshotFor("C-6000", "fold v1"));
        plain.award("C-6000", 2, "ORD-250-0", MAR_20);

        store.resetMeter();
        balance = plain.balanceFor("C-6000");
        System.out.println("  one more order, folded from the start again: " + balance
                + " points, " + store.eventsExamined() + " events read");

        store.resetMeter();
        balance = snapshotted.balanceFor("C-6000");
        System.out.println("  the same " + balance + " points, from the snapshot plus"
                + " what came after it: " + store.eventsExamined() + " event read");
        System.out.println("  that is the fix, and it is also a second place a balance"
                + " lives.");
        System.out.println("  a snapshot written by code that had a bug stays wrong"
                + " forever, which is why it records who computed it:");
        System.out.println("    " + snapshots.forCustomer("C-6000"));
        System.out.println("  the log is the truth; a snapshot is a cache you are"
                + " allowed to throw away.");
        System.out.println();
    }

    /** Act 7: the part of the bill nobody warns about until it is a legal letter. */
    private static void theBillTheErasureRequest() {
        System.out.println("Act 7 - the bill: a customer asks to be erased");

        LoyaltyEventStore store = new LoyaltyEventStore();
        SnapshotStore snapshots = new SnapshotStore();
        EventSourcedLoyaltyAccounts accounts =
                new EventSourcedLoyaltyAccounts(store, snapshots);
        marchForCustomer(accounts);
        accounts.award("C-5121", 30, "ORD-9002", MAR_8);
        snapshots.save(accounts.snapshotFor("C-5121", "fold v1"));

        // A second view of the same log, with no snapshots behind it, so the demo
        // can show what the log says and what the cache says side by side.
        EventSourcedLoyaltyAccounts logOnly = new EventSourcedLoyaltyAccounts(store);

        System.out.println("  before: C-5121 has " + accounts.balanceFor("C-5121")
                + " points, from " + store.eventsFor("C-5121").size() + " event");

        int removed = store.rewriteWithoutEventsFor("C-5121");
        System.out.println("  \"just delete the events\" removes " + removed + ":");
        System.out.println("    folding the log now gives "
                + logOnly.balanceFor("C-5121")
                + " points, and the history that explained it is gone for good");
        System.out.println("    C-4417 is untouched at " + logOnly.balanceFor(C)
                + " points, so the rest of the log survived");
        System.out.println("    but nothing touched the snapshot, and it still answers "
                + accounts.balanceFor("C-5121") + ":");
        System.out.println("      " + snapshots.forCustomer("C-5121"));
        System.out.println("  so the shop still reports a balance for a customer it just"
                + " erased, from the copy it made for speed.");
        System.out.println("  the real answers are harder: encrypt the personal fields"
                + " and destroy the key, or blank the identity and keep the event.");
        System.out.println();
    }

    /** Act 8: the event that can never be fixed, because fixing it is rewriting. */
    private static void theBillTheEventYouCanNeverChange() {
        System.out.println("Act 8 - the bill: the field somebody added in 2023");

        LoyaltyEventStore store = new LoyaltyEventStore();
        EventSourcedLoyaltyAccounts accounts = new EventSourcedLoyaltyAccounts(store);
        store.append(PointsAwarded.beforeOrderIdsWereRecorded("C-3002", 40, MAR_1));
        store.append(PointsAwarded.beforeOrderIdsWereRecorded("C-3002", 40, MAR_1));
        store.append(new PointsAwarded("C-3002", 15, "ORD-9100", MAR_8));

        for (String line : accounts.explain("C-3002")) {
            System.out.println("    " + line);
        }
        System.out.println("  the first two were written before the shop recorded order"
                + " ids, and they can never be corrected.");
        System.out.println("  so Act 3's duplicate hunt cannot see them: "
                + accounts.duplicateAwards("C-3002").size()
                + " duplicates found in a stream that has two identical awards in it.");
        System.out.println("  an event is a schema you version and never migrate, and"
                + " every reader carries the gap forever.");
        System.out.println();
    }

    /** Act 9: the confusion this project exists to end. */
    private static void eventSourcingIsNotCqrs() {
        System.out.println("Act 9 - event sourcing is not CQRS");

        CurrentStateLoyaltyAccounts rows = new CurrentStateLoyaltyAccounts();
        OrderHistoryReadModel readModel = new OrderHistoryReadModel();
        Checkout checkout = new Checkout(rows);
        checkout.placeOrder("C-7001", "ORD-9200", 40, MAR_1);
        readModel.recordOrder("C-7001", "ORD-9200", 40);

        System.out.println("  CQRS with no events anywhere:");
        System.out.println("    writes go to a row, which says "
                + rows.balanceFor("C-7001") + " points");
        System.out.println("    reads come from a second model built for the screen:");
        for (String line : readModel.historyFor("C-7001")) {
            System.out.println("      " + line);
        }

        EventSourcedLoyaltyAccounts events = marchForCustomer(
                new EventSourcedLoyaltyAccounts(new LoyaltyEventStore()));
        System.out.println("  event sourcing with no CQRS:");
        System.out.println("    writes append events, and reads fold the same events"
                + " back to " + events.balanceFor(C) + " points");
        System.out.println("    there is no second model in this project at all");
        System.out.println("  CQRS changes where reads come from. Event sourcing changes"
                + " what writes store.");
        System.out.println("  either one without the other, which is why they are two"
                + " decisions and not one.");
    }

    /**
     * C-4417's March, applied to whichever store is passed in.
     *
     * <p>The same four calls in both worlds, which is the comparison the project
     * rests on: the checkout code does not change, only what the store keeps.
     */
    private static <T extends LoyaltyAccounts> T marchForCustomer(T accounts) {
        accounts.award(C, 60, "ORD-8801", MAR_1);
        accounts.redeem(C, 25, "ORD-8814", MAR_3);
        accounts.award(C, 120, "ORD-8907", MAR_8);
        accounts.expire(C, 15, MAR_14);
        return accounts;
    }
}
