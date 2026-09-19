package com.jk.explore.aggregate.domain;

/**
 * One line of an order. It has no public constructor: the only way to make one is through
 * {@link Order#addLine}, so no line can exist that the order has not checked.
 */
public final class OrderLine {

    private final String sku;
    private final Money unitPrice;
    private final int quantity;

    OrderLine(String sku, Money unitPrice, int quantity) {
        this.sku = sku;
        this.unitPrice = unitPrice;
        this.quantity = quantity;
    }

    public String sku() {
        return sku;
    }

    public int quantity() {
        return quantity;
    }

    public Money subtotal() {
        return unitPrice.times(quantity);
    }

    Money unitPrice() {
        return unitPrice;
    }
}
