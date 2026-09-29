package com.jk.explore.objectmother;

/**
 * One line of an order: a product, how many, and the price of each.
 */
public record Line(String sku, int quantity, double price) {

    public double total() {
        return quantity * price;
    }
}
