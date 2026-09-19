package com.jk.explore.optimisticlock;

import java.util.HashMap;
import java.util.Map;

/** The store with no lock: whoever saves last replaces the whole row. */
public class LastWriteWinsStore {

    private final Map<String, Product> rows = new HashMap<>();

    public void insert(Product p) {
        rows.put(p.sku(), p);
    }

    public Product load(String sku) {
        return rows.get(sku);
    }

    public void save(Product p) {
        rows.put(p.sku(), p);
    }
}
