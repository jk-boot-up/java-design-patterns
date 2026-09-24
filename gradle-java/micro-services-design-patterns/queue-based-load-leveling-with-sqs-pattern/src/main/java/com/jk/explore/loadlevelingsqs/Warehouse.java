package com.jk.explore.loadlevelingsqs;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Where parcels are packed. It counts every parcel by order, so an order packed twice shows
 * up as two parcels, the way it would at the despatch door.
 */
public class Warehouse {

    private final Map<String, Integer> parcels = new LinkedHashMap<>();

    public synchronized void pack(String orderId) {
        parcels.merge(orderId, 1, Integer::sum);
    }

    public synchronized int parcelsFor(String orderId) {
        return parcels.getOrDefault(orderId, 0);
    }

    /** How many different orders have at least one parcel. */
    public synchronized int ordersPacked() {
        return parcels.size();
    }

    /** How many orders were packed more than once. */
    public synchronized int packedTwiceOrMore() {
        return (int) parcels.values().stream().filter(n -> n > 1).count();
    }
}
