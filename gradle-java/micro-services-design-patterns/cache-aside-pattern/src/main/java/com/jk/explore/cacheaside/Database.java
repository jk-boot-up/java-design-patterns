package com.jk.explore.cacheaside;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

/** The source of truth. Every read is counted, because reads are what the cache exists to avoid. */
public class Database {

    private final Map<String, Product> rows = new HashMap<>();
    private final AtomicInteger reads = new AtomicInteger();
    private volatile java.util.function.IntSupplier beforeRead = () -> 0;

    public synchronized void put(Product p) {
        rows.put(p.sku(), p);
    }

    public int reads() {
        return reads.get();
    }

    public void resetCount() {
        reads.set(0);
    }

    /** Lets a demo hold a read until something else has happened. */
    public void beforeEachRead(Runnable hook) {
        this.beforeRead = () -> {
            hook.run();
            return 0;
        };
    }

    public Product read(String sku) {
        beforeRead.getAsInt();
        reads.incrementAndGet();
        synchronized (this) {
            return rows.get(sku);
        }
    }
}
