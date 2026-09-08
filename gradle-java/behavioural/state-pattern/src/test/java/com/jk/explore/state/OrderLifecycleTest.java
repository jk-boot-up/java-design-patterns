package com.jk.explore.state;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * The context rather than the states: what {@link Order} records, what it
 * exposes to a caller, and what it does not have to know.
 */
class OrderLifecycleTest {

    private static Order order() {
        return new Order("A-1001", "grace@example.com", List.of(
                new OrderLine("H-100", "Wireless headphones", Money.pounds(89.99), 1),
                new OrderLine("C-220", "USB-C cable", Money.pounds(7.50), 1)));
    }

    private static List<String> statesOf(List<OrderEvent> history) {
        return history.stream().map(OrderEvent::to).toList();
    }

    @Nested
    @DisplayName("the legal path")
    class HappyPath {

        @Test
        void runsPlacedToDelivered() {
            Order order = order();

            order.pay();
            order.pack();
            order.ship();
            order.deliver();

            assertEquals(List.of("PAID", "PACKED", "SHIPPED", "DELIVERED"),
                    statesOf(order.history()));
        }

        @Test
        void recordsTheActionThatCausedEachMove() {
            Order order = order();

            order.pay();
            order.pack();

            assertEquals(List.of("pay", "pack"),
                    order.history().stream().map(OrderEvent::action).toList());
        }

        @Test
        void everyEventNamesWhereItCameFrom() {
            Order order = order();

            order.pay();
            order.pack();

            assertEquals("PLACED", order.history().get(0).from());
            assertEquals("PAID", order.history().get(1).from());
        }

        @Test
        void leavesTheShopWithTheMoneyWhenNothingGoesWrong() {
            Order order = order();

            order.pay();
            order.pack();
            order.ship();
            order.deliver();

            assertEquals(order.total(), order.ledger().net());
            assertEquals(0, order.ledger().refundCount());
        }

        @Test
        void totalIsTheSumOfTheLines() {
            assertEquals(Money.pounds(97.49), order().total());
            assertEquals(2, order().itemCount());
        }
    }

    @Nested
    @DisplayName("what a refusal leaves behind")
    class Refusals {

        @Test
        void doesNotChangeTheState() {
            Order order = order();
            order.pay();

            assertThrows(IllegalTransitionException.class, order::deliver);

            assertEquals("PAID", order.status());
            assertSame(PaidState.INSTANCE, order.state());
        }

        @Test
        void isRecordedInTheHistory() {
            Order order = order();

            assertThrows(IllegalTransitionException.class, order::ship);

            OrderEvent event = order.history().get(0);
            assertTrue(event.wasRefused());
            assertEquals("ship", event.action());
            assertEquals("PLACED", event.from());
        }

        @Test
        void namesTheStateThatRefusedRatherThanTheOneItWantedToReach() {
            Order order = order();

            IllegalTransitionException refusal =
                    assertThrows(IllegalTransitionException.class, order::deliver);

            assertEquals("PLACED", refusal.state());
            assertEquals("deliver", refusal.action());
        }

        @Test
        void saysWhatTheStateWouldHaveAccepted() {
            Order order = order();
            order.pay();

            IllegalTransitionException refusal =
                    assertThrows(IllegalTransitionException.class, order::ship);

            assertTrue(refusal.reason().contains("pack"), refusal.reason());
            assertTrue(refusal.reason().contains("cancel"), refusal.reason());
        }

        @Test
        void readsAsASentence() {
            Order order = order();

            IllegalTransitionException refusal =
                    assertThrows(IllegalTransitionException.class, order::deliver);

            assertTrue(refusal.getMessage().startsWith("cannot deliver a PLACED order:"),
                    refusal.getMessage());
        }

        @Test
        void usesTheRightArticleBeforeAVowel() {
            Order order = order();
            order.pay();
            order.pack();
            order.ship();
            order.deliver();
            order.refund("faulty");

            IllegalTransitionException refusal =
                    assertThrows(IllegalTransitionException.class, order::pay);

            assertTrue(refusal.getMessage().contains("a REFUNDED order"), refusal.getMessage());
        }
    }

    @Nested
    @DisplayName("the buttons to draw")
    class AllowedActions {

        @Test
        void comeFromTheStateItself() {
            Order order = order();

            assertEquals(List.of("pay", "cancel"), order.allowedActions());
            order.pay();
            assertEquals(List.of("pack", "cancel"), order.allowedActions());
            order.pack();
            assertEquals(List.of("ship", "cancel"), order.allowedActions());
            order.ship();
            assertEquals(List.of("deliver"), order.allowedActions());
        }

        /**
         * The point of asking the state twice: the list a screen draws and the
         * method a request calls cannot disagree, because one class answers both.
         */
        @Test
        void agreeWithWhatTheMethodsActuallyDo() {
            for (OrderState state : List.of(PlacedState.INSTANCE, PaidState.INSTANCE,
                    PackedState.INSTANCE, ShippedState.INSTANCE, DeliveredState.INSTANCE,
                    CancelledState.INSTANCE, RefundedState.INSTANCE)) {
                for (String action : List.of("pay", "pack", "ship", "deliver", "cancel", "refund")) {
                    Order order = order();
                    order.transitionTo(state, "setup", "test");

                    boolean offered = order.canDo(action);
                    boolean accepted = accepts(order, action);
                    assertEquals(offered, accepted,
                            state.name() + " offers " + action + "=" + offered
                                    + " but accepts=" + accepted);
                }
            }
        }

        private boolean accepts(Order order, String action) {
            try {
                switch (action) {
                    case "pay" -> order.pay();
                    case "pack" -> order.pack();
                    case "ship" -> order.ship();
                    case "deliver" -> order.deliver();
                    case "cancel" -> order.cancel("test");
                    default -> order.refund("test");
                }
                return true;
            } catch (IllegalTransitionException e) {
                return false;
            }
        }

        @Test
        void areEmptyOnceTheOrderIsFinished() {
            Order order = order();
            order.cancel("changed their mind");

            assertEquals(List.of(), order.allowedActions());
            assertFalse(order.canDo("refund"));
        }

        @Test
        void canBeAskedOneAtATime() {
            Order order = order();

            assertTrue(order.canDo("pay"));
            assertFalse(order.canDo("ship"));
            assertFalse(order.canDo("nonsense"));
        }
    }

    @Nested
    @DisplayName("the states themselves")
    class StateObjects {

        @Test
        void holdNoDataAndSoAreShared() {
            Order one = order();
            Order two = order();
            one.pay();
            two.pay();

            assertSame(one.state(), two.state());
        }

        @Test
        void nameThemselves() {
            assertEquals("PLACED", PlacedState.INSTANCE.name());
            assertEquals("REFUNDED", RefundedState.INSTANCE.name());
        }

        /**
         * A state written outside the package this was compiled with. Nothing
         * in {@link Order} changes to accept it — the argument for the pattern.
         */
        @Test
        void canBeAddedWithoutTouchingTheOrder() {
            OrderState atLocker = new OrderState() {
                @Override
                public String name() {
                    return "AT-LOCKER";
                }

                @Override
                public List<String> allowedActions() {
                    return List.of("deliver");
                }

                @Override
                public void deliver(Order order) {
                    order.transitionTo(DeliveredState.INSTANCE, "deliver", "collected");
                }
            };

            Order order = order();
            order.pay();
            order.pack();
            order.transitionTo(atLocker, "hand over", "left at the locker");

            assertEquals("AT-LOCKER", order.status());
            assertEquals(List.of("deliver"), order.allowedActions());
            assertThrows(IllegalTransitionException.class, () -> order.cancel("changed their mind"));

            order.deliver();
            assertEquals("DELIVERED", order.status());
        }
    }
}
