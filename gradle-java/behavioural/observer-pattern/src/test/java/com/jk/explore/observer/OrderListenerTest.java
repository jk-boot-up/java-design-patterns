package com.jk.explore.observer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

/**
 * Each listener on its own, with no {@link Order} anywhere in sight.
 *
 * <p>That absence is the assertion. Under the naive design none of these could
 * be written without constructing an order service and steering it into the
 * right transition.
 */
class OrderListenerTest {

    private final List<String> lines = new ArrayList<>();

    private OrderEvent event(OrderStatus from, OrderStatus to) {
        return new OrderEvent("A-1", from, to);
    }

    @Nested
    @DisplayName("InventoryListener")
    class Inventory {

        @Test
        @DisplayName("releases the reservation when the order ships")
        void releasesOnShipped() {
            InventoryListener listener = new InventoryListener(lines::add);

            listener.onStatusChanged(event(OrderStatus.PAID, OrderStatus.SHIPPED));

            assertEquals(1, listener.released());
            assertEquals(0, listener.restocked());
        }

        @Test
        @DisplayName("restocks when the order is cancelled")
        void restocksOnCancelled() {
            InventoryListener listener = new InventoryListener(lines::add);

            listener.onStatusChanged(event(OrderStatus.PAID, OrderStatus.CANCELLED));

            assertEquals(1, listener.restocked());
        }

        @Test
        @DisplayName("ignores the statuses it does not care about, silently")
        void ignoresOtherStatuses() {
            InventoryListener listener = new InventoryListener(lines::add);

            listener.onStatusChanged(event(OrderStatus.PLACED, OrderStatus.PAID));
            listener.onStatusChanged(event(OrderStatus.SHIPPED, OrderStatus.DELIVERED));

            assertEquals(0, listener.released());
            assertTrue(lines.isEmpty(), "an uninterested listener should say nothing");
        }
    }

    @Nested
    @DisplayName("EmailListener")
    class Email {

        @Test
        @DisplayName("sends one message per event, addressed to the customer")
        void sendsOnePerEvent() {
            EmailListener listener = new EmailListener("ada@example.com", lines::add);

            listener.onStatusChanged(event(OrderStatus.PLACED, OrderStatus.PAID));
            listener.onStatusChanged(event(OrderStatus.PAID, OrderStatus.SHIPPED));

            assertEquals(2, listener.sent());
            assertTrue(lines.get(0).contains("ada@example.com"));
        }

        @Test
        @DisplayName("the wording follows the status")
        void wordingFollowsTheStatus() {
            EmailListener listener = new EmailListener("ada@example.com", lines::add);

            listener.onStatusChanged(event(OrderStatus.PAID, OrderStatus.SHIPPED));

            assertTrue(lines.get(0).endsWith("Your order A-1 is on its way"), lines.get(0));
        }
    }

    @Nested
    @DisplayName("AnalyticsListener")
    class Analytics {

        @Test
        @DisplayName("counts every event, whatever the status")
        void countsEverything() {
            AnalyticsListener listener = new AnalyticsListener(lines::add);

            listener.onStatusChanged(event(OrderStatus.PLACED, OrderStatus.PAID));
            listener.onStatusChanged(event(OrderStatus.PAID, OrderStatus.SHIPPED));
            listener.onStatusChanged(event(OrderStatus.SHIPPED, OrderStatus.DELIVERED));

            assertEquals(3, listener.total());
            assertEquals(1, listener.countFor(OrderStatus.SHIPPED));
        }

        @Test
        @DisplayName("a status never seen counts zero rather than failing")
        void unseenStatusCountsZero() {
            assertEquals(0, new AnalyticsListener(lines::add).countFor(OrderStatus.CANCELLED));
        }
    }

    @Nested
    @DisplayName("WarehouseFeedListener")
    class WarehouseFeed {

        @Test
        @DisplayName("writes a line for the two statuses the warehouse acts on")
        void writesForPaidAndShipped() {
            WarehouseFeedListener listener = new WarehouseFeedListener(lines::add);

            listener.onStatusChanged(event(OrderStatus.PLACED, OrderStatus.PAID));
            listener.onStatusChanged(event(OrderStatus.PAID, OrderStatus.SHIPPED));

            assertEquals(List.of("A-1,PAID", "A-1,SHIPPED"), listener.feed());
        }

        @Test
        @DisplayName("writes nothing for the others")
        void writesNothingOtherwise() {
            WarehouseFeedListener listener = new WarehouseFeedListener(lines::add);

            listener.onStatusChanged(event(OrderStatus.SHIPPED, OrderStatus.DELIVERED));

            assertTrue(listener.feed().isEmpty());
        }

        @Test
        @DisplayName("the feed it hands out cannot be edited from outside")
        void feedIsACopy() {
            WarehouseFeedListener listener = new WarehouseFeedListener(lines::add);
            listener.onStatusChanged(event(OrderStatus.PLACED, OrderStatus.PAID));

            List<String> feed = listener.feed();

            assertEquals(1, feed.size());
            assertThrows(UnsupportedOperationException.class, () -> feed.add("A-1,SHIPPED"));
            assertEquals(1, listener.feed().size(), "the real feed is untouched");
        }
    }
}
