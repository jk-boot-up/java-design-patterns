package com.jk.explore.railway;

import java.util.Map;

/**
 * A shopping cart, and how far through checkout it has got.
 */
public record Cart(Map<String, Integer> items, String card, double total, String orderNumber, boolean backOrder) {

    public static Cart of(Map<String, Integer> items, String card) {
        return new Cart(items, card, 0, null, false);
    }

    Cart withTotal(double t) {
        return new Cart(items, card, t, orderNumber, backOrder);
    }

    Cart withOrder(String number) {
        return new Cart(items, card, total, number, backOrder);
    }

    Cart asBackOrder() {
        return new Cart(items, card, total, orderNumber, true);
    }
}
