package com.jk.explore.writebehind;

import java.util.HashMap;
import java.util.Map;

/**
 * Without the pattern: every change is written to the database before the customer gets an answer.
 */
public final class WriteThroughStore implements CartStore {

    private final Database db;
    private final Map<String, Map<String, Integer>> cache = new HashMap<>();

    public WriteThroughStore(Database db) {
        this.db = db;
    }

    @Override
    public int set(String cartId, String item, int quantity) {
        Map<String, Integer> cart = cache.computeIfAbsent(cartId, k -> new HashMap<>());
        if (quantity == 0) {
            cart.remove(item);
        } else {
            cart.put(item, quantity);
        }
        db.save(cartId, cart);
        return Database.MS_PER_WRITE;
    }

    @Override
    public Map<String, Integer> get(String cartId) {
        return cache.getOrDefault(cartId, Map.of());
    }
}
