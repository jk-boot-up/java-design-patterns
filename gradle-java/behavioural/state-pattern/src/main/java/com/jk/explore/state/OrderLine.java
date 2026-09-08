package com.jk.explore.state;

/** One line of an order: what it is, what it costs, and how many. */
public record OrderLine(String sku, String description, Money unitPrice, int quantity) {

    public Money total() {
        return unitPrice.times(quantity);
    }

    @Override
    public String toString() {
        return String.format("%-8s %-24s %2d x %8s = %9s",
                sku, description, quantity, unitPrice, total());
    }
}
