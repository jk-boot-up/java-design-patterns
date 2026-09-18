package com.jk.explore.eventsourcing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The first half of the bill, as numbers rather than as a warning.
 *
 * <p>These tests measure the cost of folding a long stream, show the snapshot that
 * fixes it, and then show the two ways a snapshot goes wrong. The last test is the
 * important one: it demonstrates a wrong balance that looks exactly like a right
 * one, which is the failure mode that makes snapshots worth being careful about.
 */
class SnapshotTest {

    private static final LocalDate MAR_1 = LocalDate.of(2025, 3, 1);
    private static final LocalDate MAR_20 = LocalDate.of(2025, 3, 20);

    private final LoyaltyEventStore store = new LoyaltyEventStore();

    /** Twenty customers, two hundred and fifty events each: five thousand events. */
    private void fiveThousandEvents(EventSourcedLoyaltyAccounts accounts) {
        for (int round = 0; round < 250; round++) {
            for (int customer = 0; customer < 20; customer++) {
                accounts.award("C-6" + String.format("%03d", customer), 2,
                        "ORD-" + round + "-" + customer, MAR_1);
            }
        }
    }

    @Test
    @DisplayName("without a snapshot, one balance reads the whole log")
    void foldingFromTheStartCostsTheWholeLog() {
        EventSourcedLoyaltyAccounts accounts = new EventSourcedLoyaltyAccounts(store);
        fiveThousandEvents(accounts);

        store.resetMeter();
        assertEquals(500, accounts.balanceFor("C-6000"));
        assertEquals(5_000, store.eventsExamined());
    }

    @Test
    @DisplayName("with a snapshot, the same answer reads only what came after it")
    void snapshotReadsOnlyTheTail() {
        SnapshotStore snapshots = new SnapshotStore();
        EventSourcedLoyaltyAccounts plain = new EventSourcedLoyaltyAccounts(store);
        EventSourcedLoyaltyAccounts snapshotted =
                new EventSourcedLoyaltyAccounts(store, snapshots);
        fiveThousandEvents(plain);

        snapshots.save(snapshotted.snapshotFor("C-6000", "fold v1"));
        plain.award("C-6000", 2, "ORD-250-0", MAR_20);

        store.resetMeter();
        int foldedFromStart = plain.balanceFor("C-6000");
        int fromStartReads = store.eventsExamined();

        store.resetMeter();
        int fromSnapshot = snapshotted.balanceFor("C-6000");
        int snapshotReads = store.eventsExamined();

        // Same question, same answer, three orders of magnitude apart in work.
        assertEquals(502, foldedFromStart);
        assertEquals(502, fromSnapshot);
        assertEquals(5_001, fromStartReads);
        assertEquals(1, snapshotReads);
    }

    @Test
    @DisplayName("a snapshot records who computed it, because that is what goes wrong")
    void snapshotNamesItsAuthor() {
        EventSourcedLoyaltyAccounts accounts = new EventSourcedLoyaltyAccounts(store);
        accounts.award("C-6000", 40, "ORD-9100", MAR_1);

        Snapshot snapshot = accounts.snapshotFor("C-6000", "fold v1");

        assertEquals("C-6000", snapshot.customerId());
        assertEquals(40, snapshot.balance());
        assertEquals(1, snapshot.upToPosition());
        assertEquals("fold v1", snapshot.computedBy());
        assertTrue(snapshot.toString().contains("computed by fold v1"), snapshot.toString());
    }

    @Test
    @DisplayName("a snapshot written by buggy code stays wrong, and looks right")
    void aStaleSnapshotIsSilentlyWrong() {
        SnapshotStore snapshots = new SnapshotStore();
        EventSourcedLoyaltyAccounts accounts =
                new EventSourcedLoyaltyAccounts(store, snapshots);
        Checkout checkout = new Checkout(accounts);

        checkout.shipTheDoubleAwardingRelease();
        checkout.placeOrder("C-5120", "ORD-9001", 45, MAR_1);
        checkout.shipTheFix();

        // A snapshot is taken while the wrong reading code is still in use.
        snapshots.save(accounts.snapshotFor("C-5120", "fold v1"));
        assertEquals(90, snapshots.forCustomer("C-5120").balance());

        // The repair lands. The log was always right, so the repaired fold is
        // right — and the snapshot carries the old, wrong number regardless.
        assertEquals(45, accounts.balanceWithDuplicateAwardsIgnored("C-5120"));
        assertNotEquals(snapshots.forCustomer("C-5120").balance(),
                accounts.balanceWithDuplicateAwardsIgnored("C-5120"));

        // Nothing detects it. There is no exception and no warning; a wrong
        // balance is just a number. Throwing the cache away is the whole cure,
        // and it is cheap precisely because the log kept everything.
        snapshots.discardAll();
        assertEquals(0, snapshots.size());
        assertEquals(45, accounts.balanceWithDuplicateAwardsIgnored("C-5120"));
    }

    @Test
    @DisplayName("an as-of query ignores snapshots, because a snapshot is a shortcut to now")
    void pastQueriesDoNotUseSnapshots() {
        SnapshotStore snapshots = new SnapshotStore();
        EventSourcedLoyaltyAccounts accounts =
                new EventSourcedLoyaltyAccounts(store, snapshots);
        accounts.award("C-4417", 60, "ORD-8801", MAR_1);
        snapshots.save(accounts.snapshotFor("C-4417", "fold v1"));
        accounts.award("C-4417", 120, "ORD-8907", MAR_20);

        assertEquals(180, accounts.balanceFor("C-4417"));
        assertEquals(60, accounts.balanceOn("C-4417", MAR_1));
    }
}
