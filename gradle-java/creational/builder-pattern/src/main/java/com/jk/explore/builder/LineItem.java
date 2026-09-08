package com.jk.explore.builder;

/** One line of a purchase order. Nothing to decide, so a constructor is right. */
public record LineItem(String sku, String description, Money unitPrice, int quantity) {

    public LineItem {
        if (quantity < 1) {
            throw new IllegalArgumentException("quantity must be at least 1, was " + quantity);
        }
    }

    public Money total() {
        return unitPrice.times(quantity);
    }
}
