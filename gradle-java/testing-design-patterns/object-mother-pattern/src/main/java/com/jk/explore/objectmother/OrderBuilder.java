package com.jk.explore.objectmother;

import java.util.ArrayList;
import java.util.List;

/**
 * The Test Data Builder: sensible defaults for everything, and a method for each detail a test cares about.
 * In a real project this lives in src/test.
 */
public final class OrderBuilder {

    public static final double DEFAULT_PRICE = 30.00;   // one item, under the free-shipping line of 50

    private String name = "Ana";
    private boolean vip;
    private String country = "GB";
    private final List<Line> lines = new ArrayList<>();
    private boolean giftWrap;

    public static OrderBuilder anOrder() {
        return new OrderBuilder();
    }

    public OrderBuilder vip() {
        vip = true;
        return this;
    }

    public OrderBuilder shippedTo(String country) {
        this.country = country;
        return this;
    }

    public OrderBuilder giftWrapped() {
        giftWrap = true;
        return this;
    }

    public OrderBuilder totalling(double amount) {
        lines.clear();
        lines.add(new Line("MUG", 1, amount));
        return this;
    }

    public Order build() {
        List<Line> items = lines.isEmpty() ? List.of(new Line("MUG", 1, DEFAULT_PRICE)) : List.copyOf(lines);
        return new Order(new Customer(name, name.toLowerCase() + "@example.com", vip), country, items, giftWrap);
    }
}
