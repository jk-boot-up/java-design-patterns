package com.jk.explore.inputvalidation;

/**
 * An order made only of checked values. Code that receives one never needs to check again.
 */
public record ValidOrder(Sku sku, Quantity quantity, Email email, CustomerName name) {

    public double total(double price) {
        return quantity.value() * price;
    }
}
