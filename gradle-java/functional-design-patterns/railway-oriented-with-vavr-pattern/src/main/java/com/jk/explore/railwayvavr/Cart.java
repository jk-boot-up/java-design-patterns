package com.jk.explore.railwayvavr;

import java.util.Map;

/**
 * A shopping cart, and how far through checkout it has got.
 */
public record Cart(Map<String, Integer> items, String card, double total, String orderNumber) {

    public static Cart of(Map<String, Integer> items, String card) {
        return new Cart(items, card, 0, null);
    }

    Cart withTotal(double t) {
        return new Cart(items, card, t, orderNumber);
    }

    Cart withOrder(String number) {
        return new Cart(items, card, total, number);
    }
}
