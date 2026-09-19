package com.jk.explore.optimisticlock;

import java.util.HashMap;
import java.util.Map;

/**
 * The store with an optimistic lock. Nothing is locked while people work. Each row carries a version, and a
 * save succeeds only if the row still has the version the writer read. Every success bumps the version.
 */
public class OptimisticStore {

    private final Map<String, Product> rows = new HashMap<>();
    private final Map<String, Integer> versions = new HashMap<>();

    public synchronized void insert(Product p) {
        rows.put(p.sku(), p);
        versions.put(p.sku(), 1);
    }

    public synchronized Versioned<Product> load(String sku) {
        return new Versioned<>(rows.get(sku), versions.get(sku));
    }

    /** UPDATE ... SET ..., version = version + 1 WHERE sku = ? AND version = ? */
    public synchronized Versioned<Product> save(Versioned<Product> loaded) {
        String sku = loaded.value().sku();
        if (versions.get(sku) != loaded.version()) {
            throw new StaleWrite(sku);
        }
        rows.put(sku, loaded.value());
        versions.put(sku, loaded.version() + 1);
        return new Versioned<>(loaded.value(), loaded.version() + 1);
    }
}
