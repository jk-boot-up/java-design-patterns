package com.jk.explore.recipientcamel;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Every destination's inbox, plus a switch to make one unreachable.
 */
public final class Warehouses {

    public static final List<String> ALL = List.of("north", "south", "big-items", "cold-store", "fraud-review", "gift-wrap");

    private final Map<String, List<String>> inbox = new LinkedHashMap<>();
    private final Set<String> down = new java.util.HashSet<>();

    public Warehouses() {
        ALL.forEach(n -> inbox.put(n, new ArrayList<>()));
    }

    public void deliver(String destination, Order order) {
        if (down.contains(destination)) {
            throw new IllegalStateException(destination + " is unreachable");
        }
        inbox.get(destination).add(order.id());
    }

    public List<String> reached(String orderId) {
        List<String> out = new ArrayList<>();
        inbox.forEach((name, ids) -> {
            if (ids.contains(orderId)) {
                out.add(name);
            }
        });
        return out;
    }

    public int deliveries() {
        return inbox.values().stream().mapToInt(List::size).sum();
    }

    public void clear() {
        inbox.values().forEach(List::clear);
    }

    public void setDown(String name) {
        down.add(name);
    }
}
