package com.jk.explore.iterator;

/**
 * One product in the shop's catalogue.
 *
 * <p>A record, because a product here is just the four facts about it. Prices
 * are whole pounds to keep the example about iteration rather than about
 * money.
 */
public record Product(String sku, String name, String category, int priceInPounds) {

    public Product {
        if (sku == null || sku.isBlank()) {
            throw new IllegalArgumentException("sku is required");
        }
        if (priceInPounds < 0) {
            throw new IllegalArgumentException("price cannot be negative: " + priceInPounds);
        }
    }

    @Override
    public String toString() {
        return "%s  %-22s %-9s £%d".formatted(sku, name, category, priceInPounds);
    }
}
