package com.jk.explore.observer;

import java.util.List;
import java.util.function.Consumer;

/**
 * Runs the whole story: the trap, the pattern, an extension the shipped code
 * never saw, and what happens when a listener throws.
 *
 * <p>Every line is deterministic, so the transcript in the README is the real
 * output rather than a tidied-up version of it.
 */
public final class OrderEventsDemo {

    private static final Consumer<String> OUT = System.out::println;

    /** A transport that fails, because in production they eventually do. */
    private static final Consumer<String> BROKEN_SMTP = line -> {
        throw new IllegalStateException("SMTP timeout after 30s");
    };

    public static void main(String[] args) {
        heading("1. The trap: an order service that calls each system by name");
        theTrap();

        heading("2. The pattern: the order announces, the listeners decide");
        List<OrderListener> listeners = thePattern();

        heading("3. A fifth reaction, added without touching Order");
        aFifthReaction();

        heading("4. One listener throws; the others still run");
        oneListenerThrows();

        heading("5. What the listeners ended up holding");
        totals(listeners);
    }

    // ---------------------------------------------------------------- 1

    private static void theTrap() {
        InventoryListener inventory = new InventoryListener(OUT);
        EmailListener email = new EmailListener("ada@example.com", BROKEN_SMTP);
        AnalyticsListener analytics = new AnalyticsListener(OUT);
        WarehouseFeedListener warehouseFeed = new WarehouseFeedListener(OUT);

        NaiveOrderService naive =
                new NaiveOrderService(inventory, email, analytics, warehouseFeed);

        System.out.println("Shipping A-1001 through NaiveOrderService, with a broken mail server:");
        try {
            naive.markShipped("A-1001", OrderStatus.PAID);
        } catch (RuntimeException e) {
            System.out.println("  !! " + e.getMessage());
        }
        System.out.println("  analytics recorded : " + analytics.total() + " event(s)");
        System.out.println("  warehouse feed     : " + warehouseFeed.feed());
        System.out.println("  The order shipped. The warehouse was never told.");
    }

    // ---------------------------------------------------------------- 2

    private static List<OrderListener> thePattern() {
        Order order = new Order("A-1002");

        InventoryListener inventory = new InventoryListener(OUT);
        EmailListener email = new EmailListener("grace@example.com", OUT);
        AnalyticsListener analytics = new AnalyticsListener(OUT);
        WarehouseFeedListener warehouseFeed = new WarehouseFeedListener(OUT);

        order.addListener(inventory);
        order.addListener(email);
        order.addListener(analytics);
        order.addListener(warehouseFeed);

        System.out.println("Order " + order.id() + " starts at " + order.status().label()
                + " with " + order.listenerCount() + " listeners attached.");

        for (OrderStatus next : List.of(OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED)) {
            System.out.println();
            System.out.println("order.moveTo(" + next.name() + ")");
            order.moveTo(next);
        }

        System.out.println();
        System.out.println("order.moveTo(DELIVERED)  <- already there");
        order.moveTo(OrderStatus.DELIVERED);
        System.out.println("  (no event, so nobody is told twice)");

        return List.of(inventory, email, analytics, warehouseFeed);
    }

    // ---------------------------------------------------------------- 3

    private static void aFifthReaction() {
        Order order = new Order("A-1003");
        order.addListener(new AnalyticsListener(OUT));

        // Written here, in the demo, against nothing but the interface. Order
        // was compiled long before this existed and did not need recompiling.
        order.addListener(new OrderListener() {
            @Override
            public String name() {
                return "loyalty-points";
            }

            @Override
            public void onStatusChanged(OrderEvent event) {
                if (event.to() == OrderStatus.DELIVERED) {
                    System.out.println("  [loyalty-points] credited 120 points for " + event.orderId());
                }
            }
        });

        System.out.println("order.moveTo(DELIVERED) with a listener defined in this file:");
        order.moveTo(OrderStatus.DELIVERED);
    }

    // ---------------------------------------------------------------- 4

    private static void oneListenerThrows() {
        Order order = new Order("A-1004");
        order.addListener(new InventoryListener(OUT));
        order.addListener(new EmailListener("ada@example.com", BROKEN_SMTP));
        order.addListener(new AnalyticsListener(OUT));
        order.addListener(new WarehouseFeedListener(OUT));

        System.out.println("Same broken mail server, this time behind the pattern:");
        List<ListenerFailure> failures = order.moveTo(OrderStatus.SHIPPED);

        System.out.println("  failures reported  : " + failures);
        System.out.println("  order status       : " + order.status().label());
        System.out.println("  The warehouse was told anyway.");
    }

    // ---------------------------------------------------------------- 5

    private static void totals(List<OrderListener> listeners) {
        InventoryListener inventory = (InventoryListener) listeners.get(0);
        EmailListener email = (EmailListener) listeners.get(1);
        AnalyticsListener analytics = (AnalyticsListener) listeners.get(2);
        WarehouseFeedListener warehouseFeed = (WarehouseFeedListener) listeners.get(3);

        System.out.println("inventory      released " + inventory.released()
                + ", restocked " + inventory.restocked());
        System.out.println("email          sent " + email.sent() + " message(s)");
        System.out.println("analytics      " + analytics.total() + " event(s), of which "
                + analytics.countFor(OrderStatus.SHIPPED) + " shipment(s)");
        System.out.println("warehouse-feed " + warehouseFeed.feed());
        System.out.println();
        System.out.println("Four different tallies from one sequence of transitions,");
        System.out.println("and Order knows about none of them.");
    }

    private static void heading(String text) {
        System.out.println();
        System.out.println("=== " + text + " ===");
        System.out.println();
    }

    private OrderEventsDemo() {
    }
}
