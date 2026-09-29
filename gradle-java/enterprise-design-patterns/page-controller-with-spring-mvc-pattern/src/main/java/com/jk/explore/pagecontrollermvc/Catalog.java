package com.jk.explore.pagecontrollermvc;

import java.util.Map;

/**
 * The shop's products and prices.
 */
public final class Catalog {

    static final Map<String, String> NAMES = Map.of("KETTLE-1", "steel kettle", "MUG-1", "mug");
    static final Map<String, Integer> PENCE = Map.of("KETTLE-1", 3000, "MUG-1", 800);

    static String price(String sku) {
        return NAMES.get(sku) + ", " + String.format("£%.2f", PENCE.get(sku) / 100.0);
    }

    private Catalog() {
    }
}
