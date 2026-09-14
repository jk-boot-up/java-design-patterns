package com.jk.explore.apigateway;

import java.util.HashMap;
import java.util.Map;

/** The Inventory service: how many are left. The one that says no. */
public final class InventoryService {

    private final Map<String, Integer> stock = new HashMap<>(Map.of(
            "SKU-1234", 4,
            "SKU-2001", 120,
            "SKU-2002", 0));

    public boolean inStock(String sku) {
        return stock.getOrDefault(sku, 0) > 0;
    }

    /** Used by the demo to make a product go out of stock. */
    public void setStock(String sku, int units) {
        stock.put(sku, units);
    }
}
