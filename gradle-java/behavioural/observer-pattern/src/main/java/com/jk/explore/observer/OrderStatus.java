package com.jk.explore.observer;

/**
 * Where an order has got to.
 *
 * <p>Deliberately just a list of names. Which transitions are legal, and what
 * an order is allowed to do in each of them, is the State pattern's subject,
 * not this project's -- see {@code docs/observer-pattern-explained.md}.
 */
public enum OrderStatus {

    PLACED("Placed"),
    PAID("Paid"),
    SHIPPED("Shipped"),
    DELIVERED("Delivered"),
    CANCELLED("Cancelled");

    private final String label;

    OrderStatus(String label) {
        this.label = label;
    }

    public String label() {
        return label;
    }
}
