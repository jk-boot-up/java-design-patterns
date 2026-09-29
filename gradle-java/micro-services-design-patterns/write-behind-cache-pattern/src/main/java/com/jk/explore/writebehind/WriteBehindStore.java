package com.jk.explore.writebehind;

import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Set;

/**
 * The pattern: changes go to memory at once and are written to the database later, in one batch.
 *
 * <p>Each changed cart is remembered as "dirty". {@link #flush()}, which a
 * timer would call every few seconds, writes each dirty cart once, however
 * many times it changed. If the database is down, the carts stay dirty and
 * are tried again next time. If the process crashes first, they are lost.
 */
public final class WriteBehindStore implements CartStore {

    private final Database db;
    private final Map<String, Map<String, Integer>> cache = new HashMap<>();
    private final Set<String> dirty = new LinkedHashSet<>();
    private int changesSinceFlush;

    public WriteBehindStore(Database db) {
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
        dirty.add(cartId);
        changesSinceFlush++;
        return 0;
    }

    @Override
    public Map<String, Integer> get(String cartId) {
        return cache.getOrDefault(cartId, Map.of());
    }

    /** Writes every dirty cart once; returns how many were written, or -1 if the database was down. */
    public int flush() {
        int written = 0;
        try {
            for (String id : Set.copyOf(dirty)) {
                db.save(id, cache.get(id));
                dirty.remove(id);
                written++;
            }
        } catch (IllegalStateException e) {
            return -1;
        }
        changesSinceFlush = 0;
        return written;
    }

    /** The process dies: memory is gone. Returns how many changes had not reached the database. */
    public int crash() {
        int lost = changesSinceFlush;
        cache.clear();
        dirty.clear();
        changesSinceFlush = 0;
        return lost;
    }

    public int waiting() {
        return dirty.size();
    }
}
