package com.jk.explore.writethrough;

import java.util.HashMap;
import java.util.Map;

/**
 * The pattern: every write goes through the cache, which writes the database first and then updates itself, before returning.
 *
 * <p>Reads come from the cache. Because nothing writes around it, the cache
 * never disagrees with the database. If the database refuses a write, the
 * cache is not changed either.
 */
public final class WriteThroughStore {

    private final Database db;
    private final Map<String, Long> cache = new HashMap<>();
    private int hits;
    private int misses;

    public WriteThroughStore(Database db) {
        this.db = db;
    }

    public long get(String sku) {
        Long cached = cache.get(sku);
        if (cached != null) {
            hits++;
            return cached;
        }
        misses++;
        long fromDb = db.read(sku);
        cache.put(sku, fromDb);
        return fromDb;
    }

    public void put(String sku, long pence) {
        db.write(sku, pence);   // the database first; if it fails, nothing changes
        cache.put(sku, pence);  // then the cache, before the caller carries on
    }

    public int hits() {
        return hits;
    }

    public int misses() {
        return misses;
    }

    public int size() {
        return cache.size();
    }
}
