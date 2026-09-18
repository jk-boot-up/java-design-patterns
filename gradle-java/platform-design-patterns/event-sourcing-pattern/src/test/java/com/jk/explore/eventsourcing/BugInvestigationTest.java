package com.jk.explore.eventsourcing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The strongest argument in the project: a bug investigated months after the fact,
 * with a query nobody wrote in advance, against data that was already lying there.
 */
class BugInvestigationTest {

    private static final LocalDate MAR_1 = LocalDate.of(2025, 3, 1);
    private static final LocalDate MAR_8 = LocalDate.of(2025, 3, 8);
    private static final LocalDate MAR_20 = LocalDate.of(2025, 3, 20);

    private final LoyaltyEventStore store = new LoyaltyEventStore();
    private final EventSourcedLoyaltyAccounts accounts =
            new EventSourcedLoyaltyAccounts(store);
    private final Checkout checkout = new Checkout(accounts);

    @Test
    @DisplayName("a double award leaves two events, and two events never look like one")
    void theDuplicateIsStillThere() {
        checkout.placeOrder("C-5120", "ORD-8990", 10, MAR_1);
        checkout.shipTheDoubleAwardingRelease();
        checkout.placeOrder("C-5120", "ORD-9001", 45, MAR_8);
        checkout.shipTheFix();

        assertEquals(3, store.eventsFor("C-5120").size());
        assertEquals(100, accounts.balanceFor("C-5120"));

        List<String> duplicates = accounts.duplicateAwards("C-5120");

        assertEquals(1, duplicates.size());
        assertTrue(duplicates.get(0).contains("ORD-9001"), duplicates.get(0));
        assertTrue(duplicates.get(0).contains("2 times"), duplicates.get(0));
    }

    @Test
    @DisplayName("the repair changes the reading code, and no event at all")
    void repairIsAReadNotAWrite() {
        checkout.placeOrder("C-5120", "ORD-8990", 10, MAR_1);
        checkout.shipTheDoubleAwardingRelease();
        checkout.placeOrder("C-5120", "ORD-9001", 45, MAR_8);
        checkout.shipTheFix();

        int eventsBefore = store.size();

        assertEquals(100, accounts.balanceFor("C-5120"));
        assertEquals(55, accounts.balanceWithDuplicateAwardsIgnored("C-5120"));

        // Nothing was appended, nothing was edited, nothing was removed. The
        // wrong balance and the right one come from the same three events.
        assertEquals(eventsBefore, store.size());
        assertEquals(3, store.eventsFor("C-5120").size());
    }

    @Test
    @DisplayName("customers the bug never touched are left exactly as they were")
    void innocentCustomersAreUnaffectedByTheRepair() {
        checkout.placeOrder("C-5122", "ORD-8991", 25, MAR_1);
        checkout.shipTheDoubleAwardingRelease();
        checkout.placeOrder("C-5120", "ORD-9001", 45, MAR_8);
        checkout.shipTheFix();

        assertEquals(25, accounts.balanceFor("C-5122"));
        assertEquals(25, accounts.balanceWithDuplicateAwardsIgnored("C-5122"));
        assertEquals(List.of(), accounts.duplicateAwards("C-5122"));
    }

    @Test
    @DisplayName("orders placed after the fix earn once, and the log shows the window")
    void theFixStopsNewDamageAndUndoesNone() {
        checkout.shipTheDoubleAwardingRelease();
        checkout.placeOrder("C-5120", "ORD-9001", 45, MAR_8);
        checkout.shipTheFix();
        checkout.placeOrder("C-5120", "ORD-9050", 20, MAR_20);

        // Three events: two for the doubled order, one for the clean one.
        assertEquals(3, store.eventsFor("C-5120").size());
        assertEquals(110, accounts.balanceFor("C-5120"));
        assertEquals(65, accounts.balanceWithDuplicateAwardsIgnored("C-5120"));
        assertEquals(1, accounts.duplicateAwards("C-5120").size());
    }

    @Test
    @DisplayName("the naive store, given the same bug, cannot answer the same question")
    void theRowHasNothingToInvestigate() {
        CurrentStateLoyaltyAccounts row = new CurrentStateLoyaltyAccounts();
        Checkout buggy = new Checkout(row);
        buggy.placeOrder("C-5120", "ORD-8990", 10, MAR_1);
        buggy.shipTheDoubleAwardingRelease();
        buggy.placeOrder("C-5120", "ORD-9001", 45, MAR_8);
        buggy.shipTheFix();

        // The same 100 points, and this is every fact available about them. There
        // is no duplicateAwards() to call, because there is nothing to call it on.
        assertEquals(100, row.balanceFor("C-5120"));
        assertEquals("the row says 100 points. How it got there was never written down.",
                row.explain("C-5120"));
    }
}
