package com.jk.explore.translator;

/**
 * The canonical order: the one shape the warehouse understands, whatever the order came from.
 */
public record OrderMessage(String orderId, String sku, int quantity, long pence) {

    @Override
    public String toString() {
        return orderId + " " + quantity + " x " + sku + " " + String.format("£%d.%02d", pence / 100, pence % 100);
    }
}
