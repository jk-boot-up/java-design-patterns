package com.jk.explore.command;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The comparison the project exists to make: the same two edits, undone by
 * a hand-rolled note and by a command, with different answers.
 *
 * <p>These tests assert the naive behaviour as it is, bug and all. They are
 * not a claim that it cannot be fixed — they are what "fix it" would have to
 * make go red.
 */
class NaiveCartEditorTest {

    private static final Money PRICE = Money.pounds(10.00);

    @Test
    void theNaiveEditorIsFineWhenNothingOverlaps() {
        Cart cart = new Cart();
        NaiveCartEditor editor = new NaiveCartEditor(cart);

        editor.addItem("A-1", "Item A-1", PRICE, 2);
        editor.undo();

        assertFalse(cart.contains("A-1"), "for a line that was not there, its note is enough");
    }

    @Test
    @DisplayName("undoing a merged add throws away quantities it never added")
    void theNaiveEditorLosesTheEarlierQuantity() {
        Cart cart = new Cart();
        NaiveCartEditor editor = new NaiveCartEditor(cart);

        editor.addItem("A-1", "Item A-1", PRICE, 3);
        editor.addItem("A-1", "Item A-1", PRICE, 2);
        editor.undo();

        assertEquals(0, cart.quantityOf("A-1"), "all five are gone, including the customer's first three");
    }

    @Test
    void thePatternRestoresTheSameEdit() {
        Cart cart = new Cart();
        CartHistory history = new CartHistory(cart);

        history.execute(new AddItemCommand("A-1", "Item A-1", PRICE, 3));
        history.execute(new AddItemCommand("A-1", "Item A-1", PRICE, 2));
        history.undo();

        assertEquals(3, cart.quantityOf("A-1"));
    }

    @Test
    @DisplayName("undoing a replaced coupon leaves the naive cart with none")
    void theNaiveEditorLosesTheReplacedCoupon() {
        Cart cart = new Cart();
        NaiveCartEditor editor = new NaiveCartEditor(cart);

        editor.applyCoupon(new Coupon("WELCOME10", 10));
        editor.applyCoupon(new Coupon("BLACKFRIDAY", 25));
        editor.undo();

        assertTrue(cart.coupon().isEmpty(), "the customer silently loses a discount they never touched");
    }

    @Test
    void thePatternPutsTheReplacedCouponBack() {
        Cart cart = new Cart();
        CartHistory history = new CartHistory(cart);

        history.execute(new ApplyCouponCommand(new Coupon("WELCOME10", 10)));
        history.execute(new ApplyCouponCommand(new Coupon("BLACKFRIDAY", 25)));
        history.undo();

        assertEquals("WELCOME10", cart.coupon().orElseThrow().code());
    }

    @Test
    @DisplayName("the naive editor cannot undo an edit nobody taught it about")
    void theNaiveEditorHasNoRoomForANewEdit() {
        Cart cart = new Cart();
        NaiveCartEditor editor = new NaiveCartEditor(cart);
        editor.addItem("A-1", "Item A-1", PRICE, 1);

        // Removing a line is not one of the two verbs this class has, and
        // there is no way to add one from outside: the note is a private
        // record and the switch is a private method.
        assertEquals(1, editor.pendingUndos());
        assertEquals(1, cart.lineCount());
    }
}
