package com.jk.explore.multiton;

import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

/** One warehouse per region. Ask for a region and you always get that region's one warehouse. */
public final class Warehouse {

    public static final Set<String> REGIONS = Set.of("UK", "EU", "US");

    private static final Map<String, Warehouse> INSTANCES = new ConcurrentHashMap<>();
    private static final AtomicInteger CREATED = new AtomicInteger();

    private final String region;
    private int stock = 100;

    private Warehouse(String region) {
        this.region = region;
        CREATED.incrementAndGet();
    }

    public static Warehouse of(String region) {
        if (!REGIONS.contains(region)) {
            throw new IllegalArgumentException("no warehouse in " + region);
        }
        return INSTANCES.computeIfAbsent(region, Warehouse::new);
    }

    /** Only for a caller that wants a private copy: this is what the multiton exists to stop. */
    public static Warehouse unshared(String region) {
        return new Warehouse(region);
    }

    public String region() {
        return region;
    }

    public synchronized void reserve(int quantity) {
        stock -= quantity;
    }

    public synchronized int stock() {
        return stock;
    }

    public static int created() {
        return CREATED.get();
    }

    public static int held() {
        return INSTANCES.size();
    }

    /** For tests: forget every instance and start again. */
    public static void resetAll() {
        INSTANCES.clear();
        CREATED.set(0);
    }
}
