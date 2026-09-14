package com.jk.explore.apigateway;

import java.util.List;

/**
 * One screen in the shop's mobile app, assembled from four services.
 *
 * The name and description belong to Catalog, the price to Pricing, the
 * availability to Inventory, and the suggestions to Recommendations. No single
 * service can produce this record, which is the whole reason somebody has to
 * assemble it.
 *
 * <p>{@code recommendedSkus} being empty is a normal, valid page. That is the
 * one fact the gateway leans on when Recommendations stops answering.
 */
public record ProductPage(String sku, String name, String description,
                          Money price, boolean inStock, List<String> recommendedSkus) {

    public ProductPage {
        recommendedSkus = List.copyOf(recommendedSkus);
    }

    /** True when the page was built without its suggestions. */
    public boolean isDegraded() {
        return recommendedSkus.isEmpty();
    }

    @Override
    public String toString() {
        return String.format("%s  %s  %s  %d suggestions",
                name, price, inStock ? "in stock" : "out of stock", recommendedSkus.size());
    }
}
