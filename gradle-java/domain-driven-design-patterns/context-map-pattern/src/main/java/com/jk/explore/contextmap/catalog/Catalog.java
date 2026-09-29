package com.jk.explore.contextmap.catalog;

import com.jk.explore.contextmap.kernel.Money;
import java.util.Map;

/**
 * The catalogue context: the upstream supplier of prices. Sales asks it; it knows nothing about sales.
 */
public final class Catalog {

    private static final Map<String, Money> PRICES = Map.of("KETTLE-1", new Money(3000), "MUG-1", new Money(800));

    public static Money price(String sku) {
        return PRICES.get(sku);
    }

    private Catalog() {
    }
}
