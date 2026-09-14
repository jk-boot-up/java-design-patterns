package com.jk.explore.loadbalancing;

/**
 * What the Catalog service knows. Deliberately tiny.
 *
 * It is {@code static} because every instance in the cluster answers identically —
 * that interchangeability is the precondition for balancing at all. If the three
 * instances gave different answers, choosing between them would not be a load
 * decision, it would be a bug.
 */
final class CatalogService {

    private CatalogService() {
    }

    static String productName(String sku) {
        return switch (sku) {
            case "SKU-1234" -> "Barista Pro Espresso Machine";
            case "SKU-2001" -> "Single-Origin Coffee Beans 1kg";
            case "SKU-2002" -> "Stainless Steel Milk Jug";
            default -> "Unknown product";
        };
    }
}
