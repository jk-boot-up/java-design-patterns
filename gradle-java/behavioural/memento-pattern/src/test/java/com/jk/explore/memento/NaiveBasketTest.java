package com.jk.explore.memento;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * These tests assert the <em>wrong</em> answers, on purpose.
 *
 * <p>They pin the cost of writing undo without a snapshot, so that the price
 * of that design is something the build says out loud rather than something a
 * comment claims. Fix {@link NaiveBasket} and these tests go red — which is
 * exactly what should happen, because the whole point of it is to be broken.
 */
class NaiveBasketTest {

    private NaiveBasket basket;

    @BeforeEach
    void aBasketWithThreeLinesAndAVoucher() {
        basket = new NaiveBasket();
        basket.add("USB-C cable", 9, 2);
        basket.add("Laptop stand", 34, 1);
        basket.add("Desk mat", 18, 1);
        basket.applyVoucher("SAVE5");
    }

    @Test
    void undoEmptiesTheBasketInstead() {
        basket.save();
        basket.remove("Laptop stand");

        basket.undo();

        assertEquals(0, basket.itemCount(),
                "saving an alias means undo clears the list it is restoring from");
    }

    @Test
    void undoDoesNotBringBackTheRemovedLine() {
        basket.save();
        basket.remove("Laptop stand");

        basket.undo();

        assertEquals(0, basket.lines().size());
    }

    @Test
    void theVoucherWasNeverSavedSoItSurvivesTheUndo() {
        basket.save();
        basket.applyVoucher("");

        basket.undo();

        assertEquals("", basket.voucher(),
                "the snapshot never held the voucher, so undo cannot restore it");
    }

    @Test
    void andTheTotalIsWrongInAWayNothingComplainsAbout() {
        basket.save();
        basket.remove("Laptop stand");

        basket.undo();

        assertEquals(0, basket.total());   // no exception, no log, just £0
    }
}
