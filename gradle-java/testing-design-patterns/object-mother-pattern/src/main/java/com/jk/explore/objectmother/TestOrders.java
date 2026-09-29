package com.jk.explore.objectmother;

import java.util.List;

/**
 * The Object Mother: named, ready-made orders for tests. In a real project this lives in src/test.
 */
public final class TestOrders {

    public static Order domestic() {
        return new Order(new Customer("Ana", "ana@example.com", false), "GB",
                List.of(new Line("MUG", 2, 9.99)), false);
    }

    public static Order vip() {
        return new Order(new Customer("Ben", "ben@example.com", true), "GB",
                List.of(new Line("MUG", 2, 9.99)), false);
    }

    public static Order international() {
        return new Order(new Customer("Chloé", "chloe@example.com", false), "FR",
                List.of(new Line("MUG", 2, 9.99)), false);
    }

    private TestOrders() {
    }
}
