package com.jk.explore.translatorcamel;

/**
 * The canonical order: the one shape the warehouse understands, whatever the source.
 */
public record OrderMessage(String orderId, String sku, int quantity, double price) {

    @Override
    public String toString() {
        return String.format("%s %d x %s £%.2f", orderId, quantity, sku, price);
    }
}
