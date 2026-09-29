package com.jk.explore.recipientcamel;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Who should get an order. Camel's recipientList() asks this for each order and sends a copy
 * to every endpoint in the answer.
 */
public final class RoutingTable {

    private final Map<String, String> warehouseFor = new LinkedHashMap<>(Map.of(
            "kitchen", "north", "furniture", "big-items", "chilled", "cold-store"));

    /** The recipients, as Camel endpoint addresses separated by commas. */
    public String recipients(Order order) {
        List<String> to = new ArrayList<>();
        for (String category : order.categories()) {
            String w = warehouseFor.get(category);
            if (!to.contains(w)) {
                to.add(w);
            }
        }
        if (order.pence() > 50000) {
            to.add("fraud-review");
        }
        if (order.gift()) {
            to.add("gift-wrap");
        }
        return String.join(",", to.stream().map(n -> "direct:" + n).toList());
    }

    public void assign(String category, String warehouse) {
        warehouseFor.put(category, warehouse);
    }
}
