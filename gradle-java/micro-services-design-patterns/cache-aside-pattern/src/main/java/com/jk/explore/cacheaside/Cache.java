package com.jk.explore.cacheaside;

import java.util.HashMap;
import java.util.Map;

/** A small cache with an expiry per entry, counting hits and misses. */
public class Cache {

    private record Entry(Product value, long expiresAt) {
    }

    private final Map<String, Entry> entries = new HashMap<>();
    private final Clock clock;
    private final long ttlSeconds;
    private int hits;
    private int misses;

    public Cache(Clock clock, long ttlSeconds) {
        this.clock = clock;
        this.ttlSeconds = ttlSeconds;
    }

    public synchronized Product get(String sku) {
        Entry e = entries.get(sku);
        if (e == null || e.expiresAt() <= clock.now()) {
            misses++;
            return null;
        }
        hits++;
        return e.value();
    }

    public synchronized void put(Product p) {
        entries.put(p.sku(), new Entry(p, clock.now() + ttlSeconds));
    }

    public synchronized void invalidate(String sku) {
        entries.remove(sku);
    }

    public synchronized void clear() {
        entries.clear();
    }

    public synchronized int hits() {
        return hits;
    }

    public synchronized int misses() {
        return misses;
    }
}
