package com.jk.explore.backpressure;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * For updates where only the latest matters: keeps one pending value per product and drops the older ones.
 */
public final class Conflator {

    private final Map<String, Integer> latest = new LinkedHashMap<>();
    private int received;

    public void offer(String sku, int stockLevel) {
        received++;
        latest.put(sku, stockLevel);
    }

    public Map<String, Integer> drain() {
        Map<String, Integer> out = new LinkedHashMap<>(latest);
        latest.clear();
        return out;
    }

    public int received() {
        return received;
    }
}
