package com.jk.explore.nullobject.pattern;

import com.jk.explore.nullobject.domain.Discount;

/** <strong>The null object: the same interface, doing nothing.</strong> It returns the price unchanged. */
public final class NoDiscount implements Discount {

    public static final NoDiscount INSTANCE = new NoDiscount();

    private NoDiscount() {
    }

    @Override
    public long apply(long pricePence) {
        return pricePence;
    }

    @Override
    public String name() {
        return "none";
    }
}
