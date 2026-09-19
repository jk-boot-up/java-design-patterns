package com.jk.explore.actorpattern;

import java.util.HashMap;
import java.util.Map;

/** Stock held in a plain map that any thread may change, with the read and the write done separately. */
public class SharedStock {

    private final Map<String, Integer> stock = new HashMap<>();

    public SharedStock(String sku, int count) {
        stock.put(sku, count);
    }

    /** Read, think, then write: not atomic. A pause between them, as a busy machine can make, loses a change. */
    public void reserve(String sku, int quantity, Runnable pauseBetweenReadAndWrite) {
        int left;
        synchronized (this) {
            left = stock.get(sku);
        }
        pauseBetweenReadAndWrite.run();
        synchronized (this) {
            stock.put(sku, left - quantity);
        }
    }

    public synchronized int stockOf(String sku) {
        return stock.get(sku);
    }
}
