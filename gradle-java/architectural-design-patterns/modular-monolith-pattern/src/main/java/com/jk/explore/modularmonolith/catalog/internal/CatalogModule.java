package com.jk.explore.modularmonolith.catalog.internal;

import com.jk.explore.modularmonolith.catalog.CatalogApi;
import java.util.HashMap;
import java.util.Map;

/**
 * Inside the catalogue: owns the stock table and its rule that stock never goes below zero.
 */
public final class CatalogModule implements CatalogApi {

    private final Map<String, Integer> stock = new HashMap<>(Map.of("kettle", 1, "mug", 20));

    @Override
    public boolean reserve(String sku, int qty) {
        int have = stock.getOrDefault(sku, 0);
        if (have < qty) {
            return false;
        }
        stock.put(sku, have - qty);
        return true;
    }

    @Override
    public int stock(String sku) {
        return stock.getOrDefault(sku, 0);
    }
}
