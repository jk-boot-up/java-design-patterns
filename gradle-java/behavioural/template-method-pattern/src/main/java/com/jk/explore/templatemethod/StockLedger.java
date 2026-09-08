package com.jk.explore.templatemethod;

import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * The store's own stock, held in memory. Just enough for the warehouse route
 * to be able to succeed and to be able to fail.
 */
public final class StockLedger {

    private final Map<String, Integer> onHand = new LinkedHashMap<>();
    private final Map<String, Integer> reserved = new HashMap<>();

    public StockLedger stock(String sku, int units) {
        onHand.merge(sku, units, Integer::sum);
        return this;
    }

    public int available(String sku) {
        return onHand.getOrDefault(sku, 0) - reserved.getOrDefault(sku, 0);
    }

    public int reservedFor(String sku) {
        return reserved.getOrDefault(sku, 0);
    }

    /** Holds stock for an order, or refuses. Refusing stops fulfilment. */
    public void reserve(String sku, int units) {
        if (available(sku) < units) {
            throw new FulfilmentException(
                    "only " + available(sku) + " of " + sku + " available, needed " + units);
        }
        reserved.merge(sku, units, Integer::sum);
    }
}
