package com.jk.explore.higherorder;

import java.util.ArrayList;
import java.util.List;
import java.util.function.DoubleUnaryOperator;
import java.util.function.Predicate;

/**
 * The pattern: functions that take functions, and functions that return them.
 */
public final class Catalogue {

    /** Takes a function: the one loop, with the test passed in. */
    public static List<Product> filter(List<Product> all, Predicate<Product> test) {
        List<Product> out = new ArrayList<>();
        for (Product p : all) {
            if (test.test(p)) {
                out.add(p);
            }
        }
        return out;
    }

    /** Returns a function: a test made to order. */
    public static Predicate<Product> priceBelow(double limit) {
        return p -> p.price() < limit;
    }

    public static Predicate<Product> inCategory(String category) {
        return p -> p.category().equals(category);
    }

    public static Predicate<Product> inStock() {
        return p -> p.stock() > 0;
    }

    /** Returns a price rule: take off a percentage. */
    public static DoubleUnaryOperator percentOff(double percent) {
        return price -> Math.round(price * (100 - percent)) / 100.0;
    }

    /** Returns a price rule: take off a fixed amount, never below zero. */
    public static DoubleUnaryOperator amountOff(double amount) {
        return price -> Math.max(0, price - amount);
    }

    public static List<String> names(List<Product> products) {
        return products.stream().map(Product::name).toList();
    }

    private Catalogue() {
    }
}
