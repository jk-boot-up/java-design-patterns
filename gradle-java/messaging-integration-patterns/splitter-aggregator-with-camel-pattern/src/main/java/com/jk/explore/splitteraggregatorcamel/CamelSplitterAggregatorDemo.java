package com.jk.explore.splitteraggregatorcamel;

import java.util.ArrayList;
import java.util.List;

/** Six acts, run against a real Apache Camel engine. Every number printed here is the engine's own. */
public class CamelSplitterAggregatorDemo {

    public static void main(String[] args) {
        try (Store store = new Store()) {
            one(store);
            List<Shipment> shipments = two(store);
            three(store, shipments);
            four(store);
            five(store);
            six(store);
        }
    }

    private static void one(Store store) {
        System.out.println("ONE. One picker, one order.");
        Order order = Store.order("ORD-4471");
        int total = store.onePickerTotal(order);
        System.out.println("  order " + order.id() + " has " + order.lines().size() + " lines, held in "
                + Store.WAREHOUSES.size() + " warehouses: " + String.join(", ", Store.WAREHOUSES) + ".");
        System.out.println("  one picker walks all of them, one line after another: " + store.onePicker.steps()
                + " steps of work on " + store.onePicker.threadsUsed() + " thread, and the basket comes to "
                + Money.pounds(total) + ".");
        System.out.println("  while that picker walks, the other warehouses stand idle.");
    }

    private static List<Shipment> two(Store store) {
        System.out.println("TWO. Camel splits the order.");
        store.collected.clear();
        store.checkout(Store.order("ORD-4471"), "direct:collect", "");
        List<Shipment> shipments = new ArrayList<>(store.collected);
        for (Shipment s : shipments) {
            System.out.println("  " + s.orderId() + " shipment " + s.index() + " of " + s.of() + " to "
                    + s.warehouse() + ": " + s.contents() + ", " + Money.pounds(s.pence()));
        }
        System.out.println("  Camel numbered the pieces and copied the order number onto every one of them."
                + " that number is what puts them back.");
        return shipments;
    }

    private static void three(Store store, List<Shipment> shipments) {
        System.out.println("THREE. They come back in any order.");
        int[] arrival = {3, 1, 2};
        StringBuilder order = new StringBuilder();
        for (int i : arrival) {
            order.append(i).append(" ");
            store.deliver(shipments.get(i - 1), "direct:gather");
        }
        System.out.println("  the warehouses answered in the order: " + order.toString().strip() + ".");
        Gathered done = store.results.next();
        System.out.println("  the aggregator finished, completed by: " + done.completedBy() + ". "
                + done.order().count() + " of " + done.order().expected() + " shipments: "
                + done.order().contents() + ", total " + Money.pounds(done.order().totalPence()) + ".");
        System.out.println("  the pieces arrived jumbled and the answer came out in the customer's line order.");
    }

    private static void four(Store store) {
        System.out.println("FOUR. The completion condition decides everything.");
        store.checkout(Store.order("ORD-4472"), "direct:gather", "Glasgow");
        System.out.println("  ORD-4472: Glasgow is closed and never answers. shipments back: "
                + (Store.WAREHOUSES.size() - 1) + " of " + Store.WAREHOUSES.size()
                + ". answers out of the aggregator: " + store.results.size()
                + ". orders still open: " + store.routes.ordersOpen() + ".");
        System.out.println("  the only condition on this aggregator is a count, and " + (Store.WAREHOUSES.size() - 1)
                + " is not " + Store.WAREHOUSES.size() + ". nothing comes out, and nothing ever will.");
    }

    private static void five(Store store) {
        System.out.println("FIVE. A deadline, which the simulation got for free.");
        store.checkout(Store.order("ORD-4473"), "direct:gather-with-timeout", "Glasgow");
        System.out.println("  ORD-4473: Glasgow is closed again, but this aggregator also has a deadline of "
                + StoreRoutes.TIMEOUT_MILLIS + " milliseconds, looked at every " + StoreRoutes.CHECK_MILLIS + ".");
        Gathered done = store.results.next();
        System.out.println("  the aggregator gave up on its own. completed by: " + done.completedBy() + ". "
                + done.order().count() + " of " + done.order().expected() + " shipments, missing "
                + done.order().missingWarehouses(Store.WAREHOUSES) + ", complete: " + done.order().complete()
                + ", gathered so far " + Money.pounds(done.order().totalPence()) + ".");
        System.out.println("  orders still open in that aggregator: " + store.routes.ordersOpenWithTimeout()
                + ". the wait ended without anybody asking it to.");
    }

    private static void six(Store store) {
        System.out.println("SIX. The bill.");
        for (int i = 0; i < 1000; i++) {
            store.checkout(Store.order("ORD-B-" + i), "direct:gather-bill", "Glasgow");
        }
        System.out.println("  1000 orders each missing one shipment: " + store.routes.ordersOpenInTheBill()
                + " orders held in the aggregator's memory, and a restart loses every one of them.");
        store.results.takeAll();
        store.collected.clear();
        store.checkout(Store.order("ORD-9001"), "direct:collect", "");
        List<Shipment> twice = new ArrayList<>(store.collected);
        store.deliver(twice.get(0), "direct:gather-bill");
        store.deliver(twice.get(1), "direct:gather-bill");
        store.deliver(twice.get(1), "direct:gather-bill");
        Gathered done = store.results.next();
        System.out.println("  a shipment delivered twice: Camel counts messages, not distinct pieces, so ORD-9001"
                + " completed by: " + done.completedBy() + " at " + done.order().count() + " of "
                + done.order().expected() + " lines, with " + done.order().duplicates() + " duplicate noted.");
        System.out.println("  the fold has to check for itself: " + Money.pounds(done.order().totalPence())
                + " with the check, " + Money.pounds(done.order().uncheckedTotalPence()) + " without it.");
        System.out.println("  and the order number has to be unique. two orders sharing one number are gathered"
                + " into a single answer, because that number is all the aggregator has.");
    }
}
