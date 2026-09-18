package com.jk.explore.eventsourcing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The naive version, tested fairly.
 *
 * <p>Every test in here passes, and that is the point worth taking away. The
 * current-state row is not buggy and these are not failing tests waiting to be
 * fixed by the pattern — the design does exactly what it was built to do. What
 * these tests pin down is the boundary: the balance is right, and every question
 * beyond the balance has no answer in this design at all.
 */
class CurrentStateLoyaltyAccountsTest {

    private static final LocalDate MAR_1 = LocalDate.of(2025, 3, 1);
    private static final LocalDate MAR_3 = LocalDate.of(2025, 3, 3);
    private static final LocalDate MAR_8 = LocalDate.of(2025, 3, 8);
    private static final LocalDate MAR_14 = LocalDate.of(2025, 3, 14);

    private final CurrentStateLoyaltyAccounts accounts = new CurrentStateLoyaltyAccounts();

    @Test
    @DisplayName("the balance itself is correct, which is why this design survives")
    void balanceIsCorrect() {
        accounts.award("C-4417", 60, "ORD-8801", MAR_1);
        accounts.redeem("C-4417", 25, "ORD-8814", MAR_3);
        accounts.award("C-4417", 120, "ORD-8907", MAR_8);
        accounts.expire("C-4417", 15, MAR_14);

        assertEquals(140, accounts.balanceFor("C-4417"));
    }

    @Test
    @DisplayName("but the only explanation available is the number again")
    void cannotExplainTheBalance() {
        accounts.award("C-4417", 60, "ORD-8801", MAR_1);
        accounts.award("C-4417", 80, "ORD-8907", MAR_8);

        String explanation = accounts.explain("C-4417");

        assertTrue(explanation.contains("140"), explanation);
        assertTrue(explanation.contains("never written down"), explanation);
        // The order ids went into award() and are nowhere in the answer, because
        // they are nowhere in the object.
        assertTrue(!explanation.contains("ORD-8801"), explanation);
        assertTrue(!explanation.contains("ORD-8907"), explanation);
    }

    @Test
    @DisplayName("a double award is indistinguishable from a larger order")
    void doubleAwardLooksIdenticalToAHonestOrder() {
        CurrentStateLoyaltyAccounts doubled = new CurrentStateLoyaltyAccounts();
        Checkout buggy = new Checkout(doubled);
        buggy.shipTheDoubleAwardingRelease();
        buggy.placeOrder("C-5120", "ORD-9001", 50, MAR_8);

        CurrentStateLoyaltyAccounts honest = new CurrentStateLoyaltyAccounts();
        Checkout working = new Checkout(honest);
        working.placeOrder("C-5120", "ORD-9001", 100, MAR_8);

        // Two different histories, one of them a bug, and the shop cannot tell
        // them apart afterwards because both wrote the same number.
        assertEquals(honest.balanceFor("C-5120"), doubled.balanceFor("C-5120"));
        assertEquals(honest.explain("C-5120"), doubled.explain("C-5120"));
    }

    @Test
    @DisplayName("the row cannot say what the balance was last week")
    void hasNoPast() {
        accounts.award("C-4417", 60, "ORD-8801", MAR_1);
        accounts.award("C-4417", 120, "ORD-8907", MAR_8);

        // There is no method to call. The best a caller can do is read the
        // balance, which is today's, and the dates handed to award() were
        // discarded on the way in. This test asserts the shape of that gap:
        // one number, no history, whatever day you ask on.
        assertEquals(180, accounts.balanceFor("C-4417"));
        assertEquals(1, accounts.customers().size());
    }
}
