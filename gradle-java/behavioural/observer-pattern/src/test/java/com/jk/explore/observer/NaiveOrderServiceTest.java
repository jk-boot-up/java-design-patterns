package com.jk.explore.observer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The trap, pinned down.
 *
 * <p>These tests pass. That is the uncomfortable part: the naive service does
 * what it says, and the bug in it is not a failing assertion but a missing
 * one. What each test really documents is the cost the pattern is paying to
 * remove.
 */
class NaiveOrderServiceTest {

    private final List<String> lines = new ArrayList<>();
    private final Consumer<String> brokenSmtp = line -> {
        throw new IllegalStateException("SMTP timeout after 30s");
    };

    @Test
    @DisplayName("it works, when all four systems are healthy")
    void itWorksWhenNothingIsBroken() {
        InventoryListener inventory = new InventoryListener(lines::add);
        AnalyticsListener analytics = new AnalyticsListener(lines::add);
        WarehouseFeedListener feed = new WarehouseFeedListener(lines::add);
        NaiveOrderService service = new NaiveOrderService(
                inventory, new EmailListener("ada@example.com", lines::add), analytics, feed);

        service.markShipped("A-1", OrderStatus.PAID);

        assertEquals(1, inventory.released());
        assertEquals(1, analytics.total());
        assertEquals(List.of("A-1,SHIPPED"), feed.feed());
    }

    @Test
    @DisplayName("a broken mail server stops the warehouse being told")
    void oneFailureTakesTheRestDown() {
        // This is the outage, reproduced in four lines. The email client is
        // third in a list of four; the two systems after it never run, and the
        // caller gets an exception that says nothing about the warehouse.
        AnalyticsListener analytics = new AnalyticsListener(lines::add);
        WarehouseFeedListener feed = new WarehouseFeedListener(lines::add);
        NaiveOrderService service = new NaiveOrderService(
                new InventoryListener(lines::add),
                new EmailListener("ada@example.com", brokenSmtp),
                analytics,
                feed);

        assertThrows(IllegalStateException.class,
                () -> service.markShipped("A-2", OrderStatus.PAID));

        assertEquals(0, analytics.total(), "analytics never ran");
        assertTrue(feed.feed().isEmpty(), "the warehouse was never told");
    }

    @Test
    @DisplayName("the same failure behind Order leaves the other three intact")
    void thePatternIsolatesTheSameFailure() {
        AnalyticsListener analytics = new AnalyticsListener(lines::add);
        WarehouseFeedListener feed = new WarehouseFeedListener(lines::add);
        Order order = new Order("A-3");
        order.addListener(new InventoryListener(lines::add));
        order.addListener(new EmailListener("ada@example.com", brokenSmtp));
        order.addListener(analytics);
        order.addListener(feed);

        List<ListenerFailure> failures = order.moveTo(OrderStatus.SHIPPED);

        assertEquals(1, analytics.total());
        assertEquals(List.of("A-3,SHIPPED"), feed.feed());
        assertEquals("email", failures.get(0).listenerName());
    }

    @Test
    @DisplayName("a fifth reaction needs no change to Order")
    void anUnknownListenerWorksUnchanged() {
        // Order was compiled before this class existed. If this compiles and
        // passes, the extension point is real rather than a list of four.
        Order order = new Order("A-4");
        List<String> credited = new ArrayList<>();
        order.addListener(new OrderListener() {
            @Override
            public String name() {
                return "loyalty-points";
            }

            @Override
            public void onStatusChanged(OrderEvent event) {
                if (event.to() == OrderStatus.DELIVERED) {
                    credited.add(event.orderId());
                }
            }
        });

        order.moveTo(OrderStatus.SHIPPED);
        order.moveTo(OrderStatus.DELIVERED);

        assertEquals(List.of("A-4"), credited);
    }
}
