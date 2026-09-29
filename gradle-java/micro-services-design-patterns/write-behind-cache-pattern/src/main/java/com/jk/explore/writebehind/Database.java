package com.jk.explore.writebehind;

import java.util.HashMap;
import java.util.Map;

/**
 * The slow, safe store: every write takes 20 ms and survives a crash. It can be switched off.
 */
public final class Database {

    public static final int MS_PER_WRITE = 20;

    private final Map<String, Map<String, Integer>> carts = new HashMap<>();
    private int writes;
    private boolean up = true;

    public void save(String cartId, Map<String, Integer> items) {
        if (!up) {
            throw new IllegalStateException("database unavailable");
        }
        writes++;
        carts.put(cartId, Map.copyOf(items));
    }

    public Map<String, Integer> load(String cartId) {
        return carts.getOrDefault(cartId, Map.of());
    }

    public void setUp(boolean up) {
        this.up = up;
    }

    public int writes() {
        return writes;
    }
}
