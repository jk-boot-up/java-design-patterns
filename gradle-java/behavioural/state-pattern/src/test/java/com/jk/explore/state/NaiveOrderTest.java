package com.jk.explore.state;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for the version the pattern replaces.
 *
 * <p>These pass. That is the uncomfortable part: the two bugs are pinned here
 * as the behaviour the code actually has, so that {@link OrderStateTest} can be
 * read as the same scenarios coming out differently. Nothing below is a
 * suggestion about how orders ought to work.
 */
class NaiveOrderTest {

    private static final Money TOTAL = Money.pounds(97.49);

    private static NaiveOrder order() {
        return new NaiveOrder("N-9001", TOTAL);
    }

    @Nested
    @DisplayName("the parts that are right")
    class Correct {

        @Test
        void walksTheLegalPath() {
            NaiveOrder order = order();

            order.pay();
            order.pack();
            order.ship();
            order.deliver();

            assertEquals(NaiveOrder.Status.DELIVERED, order.status());
            assertEquals(TOTAL, order.ledger().net());
        }

        @Test
        void refusesToSkipAStep() {
            assertThrows(IllegalTransitionException.class, () -> order().ship());
        }

        @Test
        void refusesToPayTwice() {
            NaiveOrder order = order();
            order.pay();

            assertThrows(IllegalTransitionException.class, order::pay);
        }

        @Test
        void refundsOnceOnADeliveredOrder() {
            NaiveOrder order = order();
            order.pay();
            order.pack();
            order.ship();
            order.deliver();

            order.refund("faulty");

            assertEquals(NaiveOrder.Status.REFUNDED, order.status());
            assertTrue(order.ledger().net().isZero());
        }
    }

    @Nested
    @DisplayName("the first drift: cancelling a parcel that is on a van")
    class ShippedIsCancellable {

        @Test
        void theCancelChainAcceptsIt() {
            NaiveOrder order = order();
            order.pay();
            order.pack();
            order.ship();

            order.cancel("customer changed their mind");

            assertEquals(NaiveOrder.Status.CANCELLED, order.status());
        }

        @Test
        void andTheMoneyGoesBackWhileTheGoodsAreStillTravelling() {
            NaiveOrder order = order();
            order.pay();
            order.pack();
            order.ship();

            order.cancel("customer changed their mind");

            assertEquals(TOTAL, order.ledger().refunded());
            assertTrue(order.ledger().net().isZero());
        }

        /** The screen and the endpoint are two different copies of the rule. */
        @Test
        void eventhoughTheScreenNeverOffersTheButton() {
            NaiveOrder order = order();
            order.pay();
            order.pack();
            order.ship();

            assertFalse(order.allowedActions().contains("cancel"));
            assertDoesNotThrow(() -> order.cancel("customer changed their mind"));
        }

        @Test
        void theSameScenarioIsRefusedByTheStateVersion() {
            Order order = new Order("A-1", "grace@example.com", java.util.List.of(
                    new OrderLine("H-100", "Wireless headphones", TOTAL, 1)));
            order.pay();
            order.pack();
            order.ship();

            assertThrows(IllegalTransitionException.class,
                    () -> order.cancel("customer changed their mind"));
            assertEquals(0, order.ledger().refundCount());
        }
    }

    @Nested
    @DisplayName("the second drift: refunding an order that was already refunded")
    class CancelledIsRefundable {

        @Test
        void theRefundChainAcceptsACancelledOrder() {
            NaiveOrder order = order();
            order.pay();
            order.cancel("out of stock");

            order.refund("support ticket 4471");

            assertEquals(NaiveOrder.Status.REFUNDED, order.status());
        }

        @Test
        void andTheShopPaysTheCustomerTwice() {
            NaiveOrder order = order();
            order.pay();
            order.cancel("out of stock");

            order.refund("support ticket 4471");

            assertEquals(2, order.ledger().refundCount());
            assertEquals(TOTAL.times(2), order.ledger().refunded());
        }

        @Test
        void leavingTheLedgerOneOrderTotalShortOfZero() {
            NaiveOrder order = order();
            order.pay();
            order.cancel("out of stock");

            order.refund("support ticket 4471");

            assertEquals(Money.zero().minus(TOTAL), order.ledger().net());
            assertEquals("-£97.49", order.ledger().net().toString());
        }

        @Test
        void theSameScenarioIsRefusedByTheStateVersion() {
            Order order = new Order("A-1", "leo@example.com", java.util.List.of(
                    new OrderLine("H-100", "Wireless headphones", TOTAL, 1)));
            order.pay();
            order.cancel("out of stock");

            assertThrows(IllegalTransitionException.class,
                    () -> order.refund("support ticket 4471"));
            assertEquals(1, order.ledger().refundCount());
        }
    }

    @Nested
    @DisplayName("the third copy of the rules")
    class AllowedActions {

        @Test
        void agreeWithTheMethodsInEveryStateButOne() {
            NaiveOrder order = order();
            assertEquals(java.util.List.of("pay", "cancel"), order.allowedActions());
            order.pay();
            assertEquals(java.util.List.of("pack", "cancel"), order.allowedActions());
            order.pack();
            assertEquals(java.util.List.of("ship", "cancel"), order.allowedActions());
        }

        @Test
        void andDisagreeInTheOneThatMatters() {
            NaiveOrder order = order();
            order.pay();
            order.pack();
            order.ship();

            assertEquals(java.util.List.of("deliver"), order.allowedActions());
            order.cancel("customer changed their mind");
            assertEquals(NaiveOrder.Status.CANCELLED, order.status());
        }

        @Test
        void areEmptyOnceTheOrderIsFinished() {
            NaiveOrder order = order();
            order.cancel("changed their mind");

            assertEquals(java.util.List.of(), order.allowedActions());
        }
    }
}
