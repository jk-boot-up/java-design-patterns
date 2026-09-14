package com.jk.explore.databaseperservice;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The order history page, built without a join.
 *
 * This is the price of the pattern, made concrete. What used to be one query is now
 * three steps: ask Orders what the customer bought, collect the skus, ask Catalog what
 * they are called, and stitch the two answers together in Java.
 *
 * <p>The stitching is worth looking at closely, because it is doing a job that a
 * database used to do for free — and doing it worse. There is no foreign key any more.
 * Nothing stops Orders from holding a sku that Catalog has never heard of, so this
 * code has to decide what to show when that happens, and its answer is
 * {@link CatalogService#UNKNOWN_PRODUCT} rather than a crash.
 *
 * <p>The next project in the category, API Composition, is about doing this assembly
 * step properly.
 */
public final class OrderHistoryPage {

    private final OrderService orders;
    private final CatalogService catalog;
    private final CallLog log;

    public OrderHistoryPage(OrderService orders, CatalogService catalog, CallLog log) {
        this.orders = orders;
        this.catalog = catalog;
        this.log = log;
    }

    /** The customer's order history: two calls and an assembly step. */
    public List<OrderHistoryRow> forCustomer(String customerId) {
        List<Order> theirOrders = orders.ordersFor(customerId);
        if (theirOrders.isEmpty()) {
            return List.of();
        }

        List<String> skus = theirOrders.stream().map(Order::sku).distinct().toList();
        Map<String, String> names = catalog.namesFor(skus);
        log.note("HistoryPage", "ASSEMBLED", theirOrders.size()
                + " row(s) from 2 services");

        List<OrderHistoryRow> rows = new ArrayList<>();
        for (Order order : theirOrders) {
            rows.add(new OrderHistoryRow(order.orderId(), order.sku(),
                    names.get(order.sku()), order.quantity()));
        }
        return rows;
    }
}
