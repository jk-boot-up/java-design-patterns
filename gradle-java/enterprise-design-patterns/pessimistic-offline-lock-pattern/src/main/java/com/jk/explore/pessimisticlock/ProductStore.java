package com.jk.explore.pessimisticlock;

import java.util.HashMap;
import java.util.Map;

/** Products, edited only by whoever holds the lock on them. */
public class ProductStore {

    public record Product(String sku, long pricePence, int stock) {
    }

    private final Map<String, Product> rows = new HashMap<>();
    private final LockManager locks;

    public ProductStore(LockManager locks) {
        this.locks = locks;
        rows.put("MUG-BLUE", new Product("MUG-BLUE", 1000, 50));
        rows.put("TEA-050", new Product("TEA-050", 500, 200));
        rows.put("ESP-001", new Product("ESP-001", 30000, 5));
    }

    public Product read(String sku) {
        return rows.get(sku);
    }

    public void write(String sku, String owner, Product changed) {
        if (!locks.holds(sku, owner)) {
            throw new IllegalStateException(owner + " does not hold the lock on " + sku + ", so the write is refused");
        }
        rows.put(sku, changed);
    }
}
