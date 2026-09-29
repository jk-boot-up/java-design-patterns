package com.jk.explore.materializedview;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The pattern: a ready-made table of every customer's order history, kept up to date from events.
 *
 * <p>Reading it is one lookup and no calls to any service. It is a copy, so it
 * can be thrown away and rebuilt by replaying the events from the start.
 */
public final class OrderHistoryView {

    /** customer -> (order -> row), in the order the orders were placed. */
    private final Map<String, Map<String, HistoryRow>> byCustomer = new HashMap<>();
    private final Map<String, Event.OrderPlaced> orders = new HashMap<>();
    private final Map<String, String> productNames = new HashMap<>();
    private int rowsRewritten;

    public void on(Event e) {
        switch (e) {
            case Event.OrderPlaced o -> {
                orders.put(o.orderId(), o);
                rows(o.customerId()).put(o.orderId(),
                        new HistoryRow(o.orderId(), nameOf(o.productId()), o.quantity(), "placed"));
            }
            case Event.OrderShipped s -> {
                Map<String, HistoryRow> rows = rows(orders.get(s.orderId()).customerId());
                HistoryRow row = rows.get(s.orderId());
                rows.put(s.orderId(), new HistoryRow(row.orderId(), row.product(), row.quantity(), "shipped"));
            }
            case Event.ProductRenamed r -> {
                productNames.put(r.productId(), r.name());
                for (Event.OrderPlaced o : orders.values()) {
                    if (o.productId().equals(r.productId())) {
                        Map<String, HistoryRow> rows = rows(o.customerId());
                        HistoryRow row = rows.get(o.orderId());
                        rows.put(o.orderId(), new HistoryRow(row.orderId(), r.name(), row.quantity(), row.status()));
                        rowsRewritten++;
                    }
                }
            }
        }
    }

    private Map<String, HistoryRow> rows(String customerId) {
        return byCustomer.computeIfAbsent(customerId, k -> new LinkedHashMap<>());
    }

    private String nameOf(String productId) {
        return productNames.getOrDefault(productId, productId);
    }

    public List<HistoryRow> myOrders(String customerId) {
        return new ArrayList<>(byCustomer.getOrDefault(customerId, Map.of()).values());
    }

    public int rowCount() {
        return byCustomer.values().stream().mapToInt(Map::size).sum();
    }

    public int rowsRewritten() {
        return rowsRewritten;
    }
}
