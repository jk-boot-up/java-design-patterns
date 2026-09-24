package com.jk.explore.competingconsumersrabbitmq;

import java.util.HashMap;
import java.util.Map;

/**
 * The warehouse's stock ledger. Picking an order starts by reserving its items here.
 *
 * <p>It exists to make one cost visible. A picker that reserves the stock and then dies
 * before saying it is done leaves the reservation behind, and the next picker to be handed
 * the same order reserves it again. The ledger counts how many times each order was reserved,
 * so a duplicate shows up as a number rather than as a surprise in the stock count.
 */
public class Stock {

    private final Map<String, Integer> reservations = new HashMap<>();

    public synchronized void reserve(PickOrder order) {
        reservations.merge(order.orderId(), 1, Integer::sum);
    }

    public synchronized int timesReserved(String orderId) {
        return reservations.getOrDefault(orderId, 0);
    }
}
