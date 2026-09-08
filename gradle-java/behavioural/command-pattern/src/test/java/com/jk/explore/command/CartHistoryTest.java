package com.jk.explore.command;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

/** The invoker: what it guarantees, and what it deliberately does not know. */
class CartHistoryTest {

    private static final Money PRICE = Money.pounds(10.00);

    private final Cart cart = new Cart();
    private final CartHistory history = new CartHistory(cart);

    private static AddItemCommand add(String sku, int quantity) {
        return new AddItemCommand(sku, "Item " + sku, PRICE, quantity);
    }

    @Nested
    @DisplayName("Undo and redo")
    class UndoAndRedo {

        @Test
        void undoingNothingIsNotAnError() {
            assertFalse(history.undo(), "an empty history simply has nothing to undo");
        }

        @Test
        void undoReversesTheMostRecentCommandOnly() {
            history.execute(add("A-1", 1));
            history.execute(add("B-2", 1));
            history.undo();

            assertTrue(cart.contains("A-1"));
            assertFalse(cart.contains("B-2"));
        }

        @Test
        void repeatedUndoWalksAllTheWayBack() {
            history.execute(add("A-1", 1));
            history.execute(add("B-2", 1));
            history.execute(new ApplyCouponCommand(new Coupon("TEN", 10)));

            while (history.undo()) {
                // unwind everything
            }

            assertEquals(0, cart.lineCount());
            assertTrue(cart.coupon().isEmpty());
            assertFalse(history.canUndo());
        }

        @Test
        void redoRunsTheUndoneCommandAgain() {
            history.execute(add("A-1", 3));
            history.undo();
            assertTrue(history.redo());

            assertEquals(3, cart.quantityOf("A-1"));
        }

        @Test
        @DisplayName("executing something new discards the redo stack")
        void aNewCommandClosesOffTheOldFuture() {
            history.execute(add("A-1", 1));
            history.undo();
            history.execute(add("B-2", 1));

            assertFalse(history.canRedo(), "the branch that was undone is no longer reachable");
        }

        @Test
        void undoThenRedoLeavesTheCartWhereItWas() {
            history.execute(add("A-1", 2));
            history.execute(new ChangeQuantityCommand("A-1", 5));
            Money before = cart.total();

            history.undo();
            history.redo();

            assertEquals(before, cart.total());
            assertEquals(5, cart.quantityOf("A-1"));
        }
    }

    @Nested
    @DisplayName("Recording")
    class Recording {

        @Test
        void theLogReadsOldestFirst() {
            history.execute(add("A-1", 1));
            history.execute(new ChangeQuantityCommand("A-1", 4));
            history.execute(new ApplyCouponCommand(new Coupon("TEN", 10)));

            assertEquals(List.of("add 1 x A-1", "set A-1 to 4", "apply coupon TEN"), history.log());
        }

        @Test
        void anUndoneCommandLeavesTheLog() {
            history.execute(add("A-1", 1));
            history.execute(add("B-2", 1));
            history.undo();

            assertEquals(List.of("add 1 x A-1"), history.log());
        }

        @Test
        @DisplayName("a command that throws is not recorded as undoable")
        void aFailedCommandIsNotRecorded() {
            assertThrows(IllegalStateException.class,
                    () -> history.execute(new RemoveItemCommand("NOPE")));

            assertEquals(0, history.undoDepth(), "undoing a half-applied edit would corrupt the cart");
        }
    }

    @Nested
    @DisplayName("What the invoker does not know")
    class Ignorance {

        @Test
        @DisplayName("a command written entirely inside this test works unchanged")
        void anUnknownCommandWorksUnchanged() {
            history.execute(add("A-1", 1));

            // Gift wrapping. Nothing in src/main has ever heard of it.
            CartCommand giftWrap = new CartCommand() {
                @Override
                public String describe() {
                    return "add gift wrapping";
                }

                @Override
                public void execute(Cart cart) {
                    cart.putLine(new CartLine("GIFT", "Gift wrapping", Money.pounds(2.50), 1));
                }

                @Override
                public void undo(Cart cart) {
                    cart.removeLine("GIFT");
                }
            };

            history.execute(giftWrap);
            assertEquals(Money.pounds(12.50), cart.total());

            history.undo();
            assertEquals(Money.pounds(10.00), cart.total());
            assertEquals(List.of("add 1 x A-1"), history.log());
        }

        @Test
        void everyCommandIsSubstitutableForEveryOther() {
            List<CartCommand> commands = List.of(
                    add("A-1", 2),
                    new ChangeQuantityCommand("A-1", 3),
                    new ApplyCouponCommand(new Coupon("TEN", 10)),
                    new RemoveItemCommand("A-1"));

            for (CartCommand command : commands) {
                history.execute(command);
            }
            Money afterEverything = cart.total();
            while (history.undo()) {
                // unwind
            }

            assertEquals(Money.zero(), afterEverything, "the cart ended up empty");
            assertEquals(Money.zero(), cart.total());
            assertEquals(0, cart.lineCount());
            assertTrue(cart.coupon().isEmpty(), "the coupon came off with the rest");
        }
    }
}
