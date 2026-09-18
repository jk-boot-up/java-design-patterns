package com.jk.explore.eventsourcing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The other half of the bill: the two costs that are not about speed.
 *
 * <p>The first is erasure. A log that is never deleted from meets a customer with a
 * legal right to be forgotten, and the obvious answer — delete their events —
 * breaks two things at once. The second is versioning. An event written in 2023 was
 * written by the code of 2023, so a field added later is simply missing from it
 * forever, and every reader from then on has to cope with both shapes.
 *
 * <p>Both of these are tested rather than described because both are easy to wave
 * away in a sentence and hard to wave away in an assertion.
 */
class ErasureAndEventVersioningTest {

    private static final LocalDate JUNE_2023 = LocalDate.of(2023, 6, 4);
    private static final LocalDate MAR_1 = LocalDate.of(2025, 3, 1);
    private static final LocalDate MAR_8 = LocalDate.of(2025, 3, 8);

    private final LoyaltyEventStore store = new LoyaltyEventStore();

    @Test
    @DisplayName("deleting a customer's events destroys the history that explained them")
    void erasureLosesTheExplanation() {
        EventSourcedLoyaltyAccounts accounts = new EventSourcedLoyaltyAccounts(store);
        accounts.award("C-4417", 60, "ORD-8801", MAR_1);
        accounts.award("C-5121", 30, "ORD-9010", MAR_1);

        assertEquals(30, accounts.balanceFor("C-5121"));
        assertEquals(1, accounts.explain("C-5121").size());

        int removed = store.rewriteWithoutEventsFor("C-5121");

        assertEquals(1, removed);
        assertEquals(0, accounts.balanceFor("C-5121"));
        assertEquals(List.of(), accounts.explain("C-5121"));
        // The rest of the log is intact, which is the one thing that did go right.
        assertEquals(60, accounts.balanceFor("C-4417"));
    }

    @Test
    @DisplayName("and a snapshot taken earlier still answers for the erased customer")
    void erasureDoesNotReachTheSnapshot() {
        SnapshotStore snapshots = new SnapshotStore();
        EventSourcedLoyaltyAccounts snapshotted =
                new EventSourcedLoyaltyAccounts(store, snapshots);
        EventSourcedLoyaltyAccounts logOnly = new EventSourcedLoyaltyAccounts(store);
        snapshotted.award("C-5121", 30, "ORD-9010", MAR_1);
        snapshots.save(snapshotted.snapshotFor("C-5121", "fold v1"));

        store.rewriteWithoutEventsFor("C-5121");

        // Folding the log says the customer has nothing, and is telling the truth
        // about the log. The cache disagrees, and is still holding the balance
        // that was supposed to be gone. Deleting from the log was never enough.
        assertEquals(0, logOnly.balanceFor("C-5121"));
        assertEquals(30, snapshots.forCustomer("C-5121").balance());
        assertEquals(30, snapshotted.balanceFor("C-5121"));
    }

    @Test
    @DisplayName("an event written before a field existed never gains that field")
    void oldEventsKeepTheirOldShape() {
        PointsAwarded legacy =
                PointsAwarded.beforeOrderIdsWereRecorded("C-4417", 40, JUNE_2023);
        PointsAwarded modern = new PointsAwarded("C-4417", 60, "ORD-8801", MAR_1);

        assertFalse(legacy.recordsItsOrder());
        assertTrue(modern.recordsItsOrder());
        // The balance still works, because points were always recorded. It is the
        // question asked later that cannot be answered for the older half.
        assertEquals(40, legacy.effectOnBalance());
        assertTrue(legacy.because().contains("this event never recorded"), legacy.because());
        assertTrue(modern.because().contains("ORD-8801"), modern.because());
    }

    @Test
    @DisplayName("so a query written today is blind to the part of the log written before it")
    void aNewQueryCannotSeeOldEvents() {
        store.append(PointsAwarded.beforeOrderIdsWereRecorded("C-4417", 40, JUNE_2023));
        store.append(PointsAwarded.beforeOrderIdsWereRecorded("C-4417", 40, JUNE_2023));
        EventSourcedLoyaltyAccounts accounts = new EventSourcedLoyaltyAccounts(store);

        // Two identical awards sit in the log, and the duplicate-detector finds
        // nothing, because it works by order id and these two never had one. The
        // balance is right, the investigation is impossible, and nothing anywhere
        // reports a problem. This is the real shape of an event schema change.
        assertEquals(80, accounts.balanceFor("C-4417"));
        assertEquals(List.of(), accounts.duplicateAwards("C-4417"));

        // Add one order placed after the field arrived, doubled, and the same
        // query finds that one immediately.
        store.append(new PointsAwarded("C-4417", 45, "ORD-9001", MAR_8));
        store.append(new PointsAwarded("C-4417", 45, "ORD-9001", MAR_8));

        assertEquals(1, accounts.duplicateAwards("C-4417").size());
        assertTrue(accounts.duplicateAwards("C-4417").get(0).contains("ORD-9001"));
    }
}
