package com.jk.explore.eventsourcing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** The pattern: the balance is derived, and that is what makes the questions answerable. */
class EventSourcedLoyaltyAccountsTest {

    private static final LocalDate MAR_1 = LocalDate.of(2025, 3, 1);
    private static final LocalDate MAR_3 = LocalDate.of(2025, 3, 3);
    private static final LocalDate MAR_8 = LocalDate.of(2025, 3, 8);
    private static final LocalDate MAR_14 = LocalDate.of(2025, 3, 14);
    private static final LocalDate MAR_20 = LocalDate.of(2025, 3, 20);

    private final LoyaltyEventStore store = new LoyaltyEventStore();
    private final EventSourcedLoyaltyAccounts accounts =
            new EventSourcedLoyaltyAccounts(store);

    private void march() {
        accounts.award("C-4417", 60, "ORD-8801", MAR_1);
        accounts.redeem("C-4417", 25, "ORD-8814", MAR_3);
        accounts.award("C-4417", 120, "ORD-8907", MAR_8);
        accounts.expire("C-4417", 15, MAR_14);
    }

    @Test
    @DisplayName("the balance is the events added up, and matches the naive version")
    void balanceIsTheFold() {
        march();

        assertEquals(140, accounts.balanceFor("C-4417"));
        assertEquals(4, store.size());

        CurrentStateLoyaltyAccounts row = new CurrentStateLoyaltyAccounts();
        row.award("C-4417", 60, "ORD-8801", MAR_1);
        row.redeem("C-4417", 25, "ORD-8814", MAR_3);
        row.award("C-4417", 120, "ORD-8907", MAR_8);
        row.expire("C-4417", 15, MAR_14);

        // Same answer to the only question the row could answer. Event sourcing
        // does not buy a different balance; it buys everything below.
        assertEquals(row.balanceFor("C-4417"), accounts.balanceFor("C-4417"));
    }

    @Test
    @DisplayName("why it is 140: one line per event, with the running total")
    void explainsTheBalance() {
        march();

        List<String> lines = accounts.explain("C-4417");

        assertEquals(4, lines.size());
        assertTrue(lines.get(0).contains("2025-03-01"), lines.get(0));
        assertTrue(lines.get(0).contains("earned 60 points on order ORD-8801"), lines.get(0));
        assertTrue(lines.get(0).endsWith("balance 60"), lines.get(0));
        assertTrue(lines.get(1).endsWith("balance 35"), lines.get(1));
        assertTrue(lines.get(2).endsWith("balance 155"), lines.get(2));
        assertTrue(lines.get(3).endsWith("balance 140"), lines.get(3));
        // The expiry is explained too, which is the call support dreads most.
        assertTrue(lines.get(3).contains("twelve-month expiry"), lines.get(3));
    }

    @Test
    @DisplayName("what it was on any past day, without anybody planning for the question")
    void answersAsOfAPastDay() {
        march();

        assertEquals(0, accounts.balanceOn("C-4417", LocalDate.of(2025, 2, 28)));
        assertEquals(60, accounts.balanceOn("C-4417", MAR_1));
        assertEquals(35, accounts.balanceOn("C-4417", MAR_3));
        assertEquals(155, accounts.balanceOn("C-4417", MAR_8));
        assertEquals(140, accounts.balanceOn("C-4417", MAR_14));
        assertEquals(140, accounts.balanceOn("C-4417", MAR_20));
    }

    @Test
    @DisplayName("the day boundary is inclusive: an event counts on the day it happened")
    void asOfIncludesTheDayItself() {
        accounts.award("C-4417", 60, "ORD-8801", MAR_8);

        assertEquals(0, accounts.balanceOn("C-4417", MAR_3));
        assertEquals(60, accounts.balanceOn("C-4417", MAR_8));
    }

    @Test
    @DisplayName("a customer with no events has a balance of zero, not an error")
    void unknownCustomerFoldsToZero() {
        march();

        assertEquals(0, accounts.balanceFor("C-9999"));
        assertEquals(List.of(), accounts.explain("C-9999"));
    }

    @Test
    @DisplayName("one customer's events do not leak into another's balance")
    void foldsPerCustomer() {
        march();
        accounts.award("C-5120", 45, "ORD-9001", MAR_8);

        assertEquals(140, accounts.balanceFor("C-4417"));
        assertEquals(45, accounts.balanceFor("C-5120"));
        assertEquals(5, store.size());
    }
}
