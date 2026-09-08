package com.jk.explore.command;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

/**
 * The commands, one at a time, against a bare {@link Cart}.
 *
 * <p>Not one test in this file mentions {@link CartHistory}. A command is
 * responsible for exactly one thing — being its own inverse — and that is
 * testable without an invoker, which is most of why the pattern is worth
 * the classes.
 */
class CartCommandTest {

    private static final Money PRICE = Money.pounds(10.00);

    private static AddItemCommand add(String sku, int quantity) {
        return new AddItemCommand(sku, "Item " + sku, PRICE, quantity);
    }

    @Nested
    @DisplayName("AddItemCommand")
    class Adding {

        @Test
        void addsALineThatWasNotThere() {
            Cart cart = new Cart();
            add("A-1", 2).execute(cart);

            assertEquals(2, cart.quantityOf("A-1"));
        }

        @Test
        void undoingAnAddOfANewLineRemovesTheLine() {
            Cart cart = new Cart();
            AddItemCommand command = add("A-1", 2);
            command.execute(cart);
            command.undo(cart);

            assertFalse(cart.contains("A-1"), "the line should be gone entirely");
        }

        @Test
        void addingToAnExistingLineMerges() {
            Cart cart = new Cart();
            add("A-1", 3).execute(cart);
            add("A-1", 2).execute(cart);

            assertEquals(5, cart.quantityOf("A-1"));
        }

        @Test
        @DisplayName("undoing a merged add restores the previous quantity, not nothing")
        void undoingAMergedAddRestoresThePreviousQuantity() {
            Cart cart = new Cart();
            add("A-1", 3).execute(cart);

            AddItemCommand second = add("A-1", 2);
            second.execute(cart);
            second.undo(cart);

            assertEquals(3, cart.quantityOf("A-1"), "the first three were not this command's to remove");
        }

        @Test
        void undoBeforeExecuteIsRefused() {
            assertThrows(IllegalStateException.class, () -> add("A-1", 1).undo(new Cart()));
        }

        @Test
        void addingNothingIsRefusedAtConstruction() {
            assertThrows(IllegalArgumentException.class, () -> add("A-1", 0));
        }
    }

    @Nested
    @DisplayName("RemoveItemCommand")
    class Removing {

        private Cart cartOfThree() {
            Cart cart = new Cart();
            add("A-1", 1).execute(cart);
            add("B-2", 1).execute(cart);
            add("C-3", 1).execute(cart);
            return cart;
        }

        @Test
        void takesTheLineOut() {
            Cart cart = cartOfThree();
            new RemoveItemCommand("B-2").execute(cart);

            assertFalse(cart.contains("B-2"));
            assertEquals(2, cart.lineCount());
        }

        @Test
        @DisplayName("undo puts the line back in the position it came from")
        void undoRestoresThePosition() {
            Cart cart = cartOfThree();
            RemoveItemCommand command = new RemoveItemCommand("B-2");
            command.execute(cart);
            command.undo(cart);

            assertEquals(List.of("A-1", "B-2", "C-3"),
                    cart.lines().stream().map(CartLine::sku).toList());
        }

        @Test
        void undoRestoresTheQuantityTheLineHad() {
            Cart cart = new Cart();
            add("A-1", 7).execute(cart);

            RemoveItemCommand command = new RemoveItemCommand("A-1");
            command.execute(cart);
            command.undo(cart);

            assertEquals(7, cart.quantityOf("A-1"));
        }

        @Test
        void removingSomethingAbsentFailsLoudly() {
            assertThrows(IllegalStateException.class,
                    () -> new RemoveItemCommand("NOPE").execute(new Cart()));
        }
    }

    @Nested
    @DisplayName("ChangeQuantityCommand")
    class ChangingQuantity {

        @Test
        void setsTheQuantity() {
            Cart cart = new Cart();
            add("A-1", 1).execute(cart);
            new ChangeQuantityCommand("A-1", 6).execute(cart);

            assertEquals(6, cart.quantityOf("A-1"));
        }

        @Test
        void undoPutsTheOldQuantityBack() {
            Cart cart = new Cart();
            add("A-1", 4).execute(cart);

            ChangeQuantityCommand command = new ChangeQuantityCommand("A-1", 9);
            command.execute(cart);
            command.undo(cart);

            assertEquals(4, cart.quantityOf("A-1"));
        }

        @Test
        void keepsTheUnitPriceTheCustomerSaw() {
            Cart cart = new Cart();
            new AddItemCommand("A-1", "Item A-1", Money.pounds(3.00), 1).execute(cart);
            new ChangeQuantityCommand("A-1", 2).execute(cart);

            assertEquals(Money.pounds(6.00), cart.total());
        }

        @Test
        @DisplayName("a quantity of zero is refused rather than treated as a removal")
        void zeroIsRefused() {
            assertThrows(IllegalArgumentException.class, () -> new ChangeQuantityCommand("A-1", 0));
        }

        @Test
        void changingSomethingAbsentFailsLoudly() {
            assertThrows(IllegalStateException.class,
                    () -> new ChangeQuantityCommand("NOPE", 2).execute(new Cart()));
        }
    }

    @Nested
    @DisplayName("ApplyCouponCommand")
    class ApplyingACoupon {

        @Test
        void discountsTheSubtotal() {
            Cart cart = new Cart();
            add("A-1", 10).execute(cart);                       // £100.00
            new ApplyCouponCommand(new Coupon("TEN", 10)).execute(cart);

            assertEquals(Money.pounds(90.00), cart.total());
        }

        @Test
        void undoLeavesNoCouponWhenThereWasNone() {
            Cart cart = new Cart();
            ApplyCouponCommand command = new ApplyCouponCommand(new Coupon("TEN", 10));
            command.execute(cart);
            command.undo(cart);

            assertTrue(cart.coupon().isEmpty());
        }

        @Test
        @DisplayName("undo restores the coupon that was replaced, not no coupon")
        void undoRestoresTheReplacedCoupon() {
            Cart cart = new Cart();
            new ApplyCouponCommand(new Coupon("WELCOME10", 10)).execute(cart);

            ApplyCouponCommand better = new ApplyCouponCommand(new Coupon("BLACKFRIDAY", 25));
            better.execute(cart);
            better.undo(cart);

            assertEquals("WELCOME10", cart.coupon().orElseThrow().code());
        }

        @Test
        void undoBeforeExecuteIsRefused() {
            ApplyCouponCommand command = new ApplyCouponCommand(new Coupon("TEN", 10));
            assertThrows(IllegalStateException.class, () -> command.undo(new Cart()));
        }

        @Test
        void anImpossibleDiscountIsRefused() {
            assertThrows(IllegalArgumentException.class, () -> new Coupon("FREE", 0));
        }
    }
}
