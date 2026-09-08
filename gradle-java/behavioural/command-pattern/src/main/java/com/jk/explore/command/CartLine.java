package com.jk.explore.command;

import java.util.Objects;

/**
 * One line of a cart: a product, its unit price, and how many are in the
 * basket.
 *
 * <p>The unit price is stored on the line rather than looked up, because a
 * cart edit that is undone six steps later has to restore the price the
 * customer actually saw, not today's.
 */
public record CartLine(String sku, String name, Money unitPrice, int quantity) {

    public CartLine {
        Objects.requireNonNull(sku, "sku");
        Objects.requireNonNull(name, "name");
        Objects.requireNonNull(unitPrice, "unitPrice");
        if (quantity < 1) {
            throw new IllegalArgumentException(
                    "a cart line needs at least one item, was " + quantity);
        }
    }

    /** The same line with a different quantity. Lines are values; nothing is mutated. */
    public CartLine withQuantity(int newQuantity) {
        return new CartLine(sku, name, unitPrice, newQuantity);
    }

    public Money lineTotal() {
        return unitPrice.times(quantity);
    }

    @Override
    public String toString() {
        return String.format("%-8s %-22s %2d x %8s = %9s",
                sku, name, quantity, unitPrice, lineTotal());
    }
}
