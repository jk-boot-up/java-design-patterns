package com.jk.explore.materializedview;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * The three services that own the data: orders, shipping and the catalogue, each counting its calls.
 *
 * <p>Every call is counted as 40 ms, a typical network round trip, so the
 * demo can add up the waiting without actually sleeping.
 */
public final class Services {

    public static final int MS_PER_CALL = 40;

    private final Map<String, List<Event.OrderPlaced>> ordersByCustomer = new HashMap<>();
    private final Map<String, Boolean> shipped = new HashMap<>();
    private final Map<String, String> productNames = new HashMap<>();
    private int calls;
    private boolean catalogueUp = true;

    /** Each service applies its own events; this is its own data, not a copy. */
    public void apply(Event e) {
        switch (e) {
            case Event.OrderPlaced o -> ordersByCustomer.computeIfAbsent(o.customerId(), k -> new ArrayList<>()).add(o);
            case Event.OrderShipped s -> shipped.put(s.orderId(), true);
            case Event.ProductRenamed r -> productNames.put(r.productId(), r.name());
        }
    }

    public List<Event.OrderPlaced> ordersOf(String customerId) {
        calls++;
        return ordersByCustomer.getOrDefault(customerId, List.of());
    }

    public boolean isShipped(String orderId) {
        calls++;
        return shipped.getOrDefault(orderId, false);
    }

    public String productName(String productId) {
        calls++;
        if (!catalogueUp) {
            throw new IllegalStateException("catalogue service unavailable");
        }
        return productNames.get(productId);
    }

    public void setCatalogueUp(boolean up) {
        catalogueUp = up;
    }

    public int calls() {
        return calls;
    }
}
