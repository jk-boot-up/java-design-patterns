package com.jk.explore.pagecontroller;

import java.util.Map;

/**
 * The shop's catalogue, shared by the pages.
 */
public final class Shop {

    static final Map<String, String> PRODUCTS = Map.of("KETTLE-1", "steel kettle, £30.00", "MUG-1", "mug, £8.00");

    public static String describe(String sku) {
        return PRODUCTS.getOrDefault(sku, "unknown");
    }

    private Shop() {
    }
}
