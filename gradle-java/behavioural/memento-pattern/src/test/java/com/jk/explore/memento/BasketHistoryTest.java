package com.jk.explore.memento;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/** The caretaker: stacking snapshots up and stepping back through them. */
class BasketHistoryTest {

    private Basket basket;
    private BasketHistory history;

    @BeforeEach
    void setUp() {
        basket = new Basket();
        history = new BasketHistory();
    }

    @Test
    void aFreshHistoryHasNothingToUndo() {
        assertFalse(history.canUndo());
        assertThrows(IllegalStateException.class, () -> history.undo(basket));
    }

    @Test
    void undoStepsBackOneChangeAtATime() {
        history.record(basket, "added the cable");
        basket.add("USB-C cable", 9, 2);
        history.record(basket, "added the stand");
        basket.add("Laptop stand", 34, 1);
        assertEquals(3, basket.itemCount());

        assertEquals("added the stand", history.undo(basket));
        assertEquals(2, basket.itemCount());

        assertEquals("added the cable", history.undo(basket));
        assertEquals(0, basket.itemCount());
        assertFalse(history.canUndo());
    }

    @Test
    void snapshotsAreCappedSoALongSessionDoesNotGrowForever() {
        for (int i = 0; i < 50; i++) {
            history.record(basket, "change " + i);
            basket.add("Desk mat", 18, 1);
        }
        assertEquals(20, history.size());

        // The oldest ones were dropped, so the newest is still the next undo.
        assertEquals("change 49", history.undo(basket));
    }

    @Test
    void undoRestoresTheVoucherAsWellAsTheLines() {
        basket.add("Desk mat", 18, 1);
        basket.applyVoucher("SAVE5");

        history.record(basket, "cleared the basket");
        basket.remove("Desk mat");
        basket.applyVoucher("");

        history.undo(basket);

        assertEquals(1, basket.itemCount());
        assertEquals("SAVE5", basket.voucher());
        assertTrue(basket.total() == 13);
    }
}
