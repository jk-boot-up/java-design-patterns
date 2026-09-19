package com.jk.explore.contract;

import java.util.Map;

/** The catalog's price service. Each release answers in its own shape. */
public interface PriceProvider {

    Map<String, Object> price(String sku);

    /** The first release: sku, priceCents in pence, currency. */
    static PriceProvider v1() {
        return sku -> Map.of("sku", sku, "priceCents", 1600, "currency", "GBP");
    }

    /** A release that renames priceCents to price. */
    static PriceProvider renamed() {
        return sku -> Map.of("sku", sku, "price", 1600, "currency", "GBP");
    }

    /** A release that only adds a field. */
    static PriceProvider extraField() {
        return sku -> Map.of("sku", sku, "priceCents", 1600, "currency", "GBP", "stock", 40);
    }

    /** A release that keeps the field and its type, but now means pounds, not pence. */
    static PriceProvider pounds() {
        return sku -> Map.of("sku", sku, "priceCents", 16, "currency", "GBP");
    }
}
