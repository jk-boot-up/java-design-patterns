package com.jk.explore.mvpmvvm;

import java.util.ArrayList;
import java.util.List;

/** The model: what is in the cart. It knows nothing about screens. */
public class Cart {

    private final List<Long> prices = new ArrayList<>();

    public void add(long priceCents) {
        prices.add(priceCents);
    }

    public void removeLast() {
        if (!prices.isEmpty()) {
            prices.remove(prices.size() - 1);
        }
    }

    public long totalCents() {
        return prices.stream().mapToLong(Long::longValue).sum();
    }

    public int count() {
        return prices.size();
    }

    public static String money(long cents) {
        return String.format("£%d.%02d", cents / 100, cents % 100);
    }
}
