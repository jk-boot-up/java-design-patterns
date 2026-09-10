package com.jk.explore.memento;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/** The originator: what a snapshot captures, and what it survives. */
class BasketTest {

    private Basket basket;

    @BeforeEach
    void aBasketWithThreeLinesAndAVoucher() {
        basket = new Basket();
        basket.add("USB-C cable", 9, 2);
        basket.add("Laptop stand", 34, 1);
        basket.add("Desk mat", 18, 1);
        basket.applyVoucher("SAVE5");
    }

    @Test
    void restoreBringsBackARemovedLine() {
        BasketSnapshot before = basket.save("removed the laptop stand");
        basket.remove("Laptop stand");
        assertEquals(3, basket.itemCount());

        basket.restore(before);

        assertEquals(4, basket.itemCount());
        assertEquals(65, basket.total());   // 18 + 34 + 18, less the £5 voucher
    }

    @Test
    void restoreBringsBackTheVoucherToo() {
        BasketSnapshot before = basket.save("removed the voucher");
        basket.applyVoucher("");
        assertEquals(70, basket.total());

        basket.restore(before);

        assertEquals("SAVE5", basket.voucher());
        assertEquals(65, basket.total());
    }

    @Test
    void laterChangesCannotReachBackIntoAnOlderSnapshot() {
        // The point of copying rather than aliasing. Everything below happens
        // after the snapshot is taken, and none of it may affect it.
        BasketSnapshot before = basket.save("emptied the basket");
        basket.remove("USB-C cable");
        basket.remove("Laptop stand");
        basket.remove("Desk mat");
        basket.applyVoucher("");
        assertEquals(0, basket.itemCount());

        basket.restore(before);

        assertEquals(4, basket.itemCount());
        assertEquals("SAVE5", basket.voucher());
    }

    @Test
    void restoringDoesNotUseTheSnapshotUp() {
        BasketSnapshot before = basket.save("removed the desk mat");

        basket.remove("Desk mat");
        basket.restore(before);
        basket.remove("Desk mat");
        basket.restore(before);   // the same snapshot, a second time

        assertEquals(4, basket.itemCount());
    }

    @Test
    void theLabelIsCarriedAlongForTheHistoryList() {
        assertEquals("removed the laptop stand",
                basket.save("removed the laptop stand").label());
    }

    @Test
    void anEmptyBasketSnapshotsJustAsHappily() {
        Basket empty = new Basket();
        BasketSnapshot nothing = empty.save("start");
        empty.add("Desk mat", 18, 1);

        empty.restore(nothing);

        assertEquals(0, empty.itemCount());
        assertTrue(empty.lines().isEmpty());
    }
}
