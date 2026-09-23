package com.jk.explore.splitteraggregatorcamel;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 * The half-finished answer for one order while the aggregator is still waiting. It holds the shipments that
 * have come back so far, keyed by their place in the order, so that the answer comes out in the customer's
 * line order however jumbled the arrivals were. A shipment that arrives a second time is counted once and
 * noted as a duplicate; the running total that would have been charged without that check is kept alongside,
 * so the demo can show what the check is protecting the customer from.
 */
public final class Gathering {

    private final String orderId;
    private final int expected;
    private final Map<Integer, Shipment> received = new TreeMap<>();
    private int duplicates;
    private int uncheckedPence;

    public Gathering(String orderId, int expected) {
        this.orderId = orderId;
        this.expected = expected;
    }

    public void add(Shipment shipment) {
        uncheckedPence += shipment.pence();
        if (received.putIfAbsent(shipment.index(), shipment) != null) {
            duplicates++;
        }
    }

    public String orderId() {
        return orderId;
    }

    public int expected() {
        return expected;
    }

    public int count() {
        return received.size();
    }

    public int duplicates() {
        return duplicates;
    }

    public int totalPence() {
        return received.values().stream().mapToInt(Shipment::pence).sum();
    }

    /** What the customer would have been charged if a repeated shipment had simply been added on. */
    public int uncheckedTotalPence() {
        return uncheckedPence;
    }

    public List<String> contents() {
        List<String> out = new ArrayList<>();
        received.values().forEach(s -> out.add(s.describe()));
        return out;
    }

    /** The warehouses whose shipment never came back, named rather than numbered. */
    public List<String> missingWarehouses(List<String> all) {
        List<String> out = new ArrayList<>();
        for (int i = 1; i <= expected; i++) {
            if (!received.containsKey(i)) {
                out.add(all.get(i - 1));
            }
        }
        return out;
    }

    /** The places in the order that never came back. */
    public List<Integer> missing() {
        List<Integer> out = new ArrayList<>();
        for (int i = 1; i <= expected; i++) {
            if (!received.containsKey(i)) {
                out.add(i);
            }
        }
        return out;
    }

    public boolean complete() {
        return missing().isEmpty();
    }
}
