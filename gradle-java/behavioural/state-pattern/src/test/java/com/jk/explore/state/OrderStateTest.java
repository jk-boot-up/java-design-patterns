package com.jk.explore.state;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * One nested group per state, testing what that state accepts and what it
 * refuses.
 *
 * <p>The refusals matter as much as the transitions. Every one of them is the
 * absence of an override rather than a check somebody wrote, so a test that
 * only walked the happy path would prove nothing about them.
 */
class OrderStateTest {

    private static final Money TOTAL = Money.pounds(97.49);

    private Order order;

    @BeforeEach
    void setUp() {
        order = new Order("A-1", "grace@example.com", List.of(
                new OrderLine("H-100", "Wireless headphones", Money.pounds(89.99), 1),
                new OrderLine("C-220", "USB-C cable", Money.pounds(7.50), 1)));
    }

    private IllegalTransitionException refusalOf(Runnable request) {
        return assertThrows(IllegalTransitionException.class, request::run);
    }

    @Nested
    @DisplayName("PLACED")
    class Placed {

        @Test
        void startsThere() {
            assertEquals("PLACED", order.status());
            assertSame(PlacedState.INSTANCE, order.state());
        }

        @Test
        void payingChargesTheTotalAndMovesToPaid() {
            order.pay();

            assertEquals("PAID", order.status());
            assertEquals(TOTAL, order.ledger().charged());
        }

        @Test
        void cancellingRefundsNothingBecauseNothingWasTaken() {
            order.cancel("changed their mind");

            assertEquals("CANCELLED", order.status());
            assertEquals(0, order.ledger().refundCount());
            assertTrue(order.ledger().net().isZero());
        }

        @Test
        void cannotBePacked() {
            assertEquals("PLACED", refusalOf(order::pack).state());
        }

        @Test
        void cannotBeShipped() {
            assertEquals("PLACED", refusalOf(order::ship).state());
        }

        @Test
        void cannotBeRefundedBeforeItWasEverPaidFor() {
            assertEquals("refund", refusalOf(() -> order.refund("why")).action());
        }
    }

    @Nested
    @DisplayName("PAID")
    class Paid {

        @BeforeEach
        void pay() {
            order.pay();
        }

        @Test
        void packingMovesToPackedAndCountsTheItems() {
            order.pack();

            assertEquals("PACKED", order.status());
            assertTrue(lastDetail().contains("2 item(s)"));
        }

        @Test
        void cancellingGivesTheMoneyBack() {
            order.cancel("out of stock");

            assertEquals("CANCELLED", order.status());
            assertEquals(TOTAL, order.ledger().refunded());
            assertTrue(order.ledger().net().isZero());
        }

        @Test
        void cannotBePaidTwice() {
            IllegalTransitionException refusal = refusalOf(order::pay);

            assertEquals("PAID", refusal.state());
            assertEquals(TOTAL, order.ledger().charged());
        }

        @Test
        void cannotBeShippedBeforeItIsPacked() {
            assertEquals("PAID", refusalOf(order::ship).state());
        }
    }

    @Nested
    @DisplayName("PACKED")
    class Packed {

        @BeforeEach
        void packIt() {
            order.pay();
            order.pack();
        }

        @Test
        void shippingRecordsAConsignmentNumber() {
            order.ship();

            assertEquals("SHIPPED", order.status());
            assertEquals("CON-A-1", order.consignment());
        }

        @Test
        void cancellingRefundsAndSaysTheBoxWasOpened() {
            order.cancel("customer rang");

            assertEquals("CANCELLED", order.status());
            assertEquals(TOTAL, order.ledger().refunded());
            assertTrue(lastDetail().contains("stock returned"));
        }

        @Test
        void cannotBeDeliveredWithoutBeingShipped() {
            assertEquals("PACKED", refusalOf(order::deliver).state());
        }
    }

    @Nested
    @DisplayName("SHIPPED")
    class Shipped {

        @BeforeEach
        void shipIt() {
            order.pay();
            order.pack();
            order.ship();
        }

        @Test
        void deliveringQuotesTheConsignment() {
            order.deliver();

            assertEquals("DELIVERED", order.status());
            assertTrue(lastDetail().contains("CON-A-1"));
        }

        /** The transition the naive version allows, and the reason for the project. */
        @Test
        void cannotBeCancelled() {
            IllegalTransitionException refusal =
                    refusalOf(() -> order.cancel("changed their mind"));

            assertEquals("SHIPPED", refusal.state());
            assertTrue(refusal.reason().contains("courier"), refusal.reason());
        }

        @Test
        void cancellingRefundsNothing() {
            assertThrows(IllegalTransitionException.class,
                    () -> order.cancel("changed their mind"));

            assertEquals(0, order.ledger().refundCount());
            assertEquals(TOTAL, order.ledger().net());
        }

        @Test
        void cannotBeRefundedUntilItHasArrived() {
            assertEquals("SHIPPED", refusalOf(() -> order.refund("faulty")).state());
        }
    }

    @Nested
    @DisplayName("DELIVERED")
    class Delivered {

        @BeforeEach
        void deliverIt() {
            order.pay();
            order.pack();
            order.ship();
            order.deliver();
        }

        @Test
        void refundingReturnsTheMoneyOnceAndOnly() {
            order.refund("faulty on arrival");

            assertEquals("REFUNDED", order.status());
            assertEquals(1, order.ledger().refundCount());
            assertTrue(order.ledger().net().isZero());
        }

        @Test
        void cannotBeCancelledBecauseTheCustomerHasIt() {
            IllegalTransitionException refusal =
                    refusalOf(() -> order.cancel("changed their mind"));

            assertTrue(refusal.reason().contains("return"), refusal.reason());
        }

        @Test
        void cannotBeDeliveredTwice() {
            assertEquals("DELIVERED", refusalOf(order::deliver).state());
        }
    }

    @Nested
    @DisplayName("the terminal states")
    class Terminal {

        @Test
        void cancelledAcceptsNothingAtAll() {
            order.cancel("changed their mind");

            assertEquals(List.of(), order.allowedActions());
            assertThrows(IllegalTransitionException.class, order::pay);
            assertThrows(IllegalTransitionException.class, order::pack);
            assertThrows(IllegalTransitionException.class, order::ship);
            assertThrows(IllegalTransitionException.class, order::deliver);
            assertThrows(IllegalTransitionException.class, () -> order.cancel("again"));
            assertThrows(IllegalTransitionException.class, () -> order.refund("again"));
        }

        /** The naive version's second bug: a cancelled order refunded a second time. */
        @Test
        void aCancelledOrderCannotBeRefundedAgain() {
            order.pay();
            order.cancel("out of stock");
            Money after = order.ledger().net();

            assertThrows(IllegalTransitionException.class, () -> order.refund("ticket 4471"));

            assertEquals(1, order.ledger().refundCount());
            assertEquals(after, order.ledger().net());
        }

        @Test
        void refundedAcceptsNothingEither() {
            order.pay();
            order.pack();
            order.ship();
            order.deliver();
            order.refund("faulty");

            assertEquals(List.of(), order.allowedActions());
            assertThrows(IllegalTransitionException.class, () -> order.refund("again"));
        }

        @Test
        void theRefusalExplainsThatTheOrderIsFinal() {
            order.cancel("changed their mind");

            assertTrue(refusalOf(() -> order.refund("x")).reason().contains("final"));
        }
    }

    private String lastDetail() {
        List<OrderEvent> history = order.history();
        return history.get(history.size() - 1).detail();
    }
}
