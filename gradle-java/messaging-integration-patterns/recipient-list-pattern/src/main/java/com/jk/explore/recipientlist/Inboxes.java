package com.jk.explore.recipientlist;

import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

/**
 * Every destination's inbox, and which destinations are currently unreachable.
 */
public final class Inboxes {

    private final Map<String, List<String>> inbox = new TreeMap<>();
    private final Set<String> down = new HashSet<>();

    public boolean deliver(String destination, Order order) {
        if (down.contains(destination)) {
            return false;
        }
        inbox.computeIfAbsent(destination, k -> new java.util.ArrayList<>()).add(order.id());
        return true;
    }

    public void takeDown(String destination) {
        down.add(destination);
    }

    public Map<String, List<String>> all() {
        return new LinkedHashMap<>(inbox);
    }

    public int total() {
        return inbox.values().stream().mapToInt(List::size).sum();
    }
}
