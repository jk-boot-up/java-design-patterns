package com.jk.explore.templatemethod;

/**
 * One line of an order: what was bought, at what price, how many times over.
 *
 * <p>A record because it is data and nothing else. Nothing in this project
 * changes a line once the order exists — fulfilment reads the order, it does
 * not edit it.
 */
public record OrderLine(String sku, String description, Money unitPrice, int quantity) {

    public OrderLine {
        if (sku == null || sku.isBlank()) {
            throw new IllegalArgumentException("a line needs a SKU");
        }
        if (quantity < 1) {
            throw new IllegalArgumentException("a line needs at least one unit: " + sku);
        }
    }

    /** Unit price times quantity. */
    public Money total() {
        return unitPrice.times(quantity);
    }

    @Override
    public String toString() {
        return String.format("%-8s %-24s %2d x %8s = %9s",
                sku, description, quantity, unitPrice, total());
    }
}
