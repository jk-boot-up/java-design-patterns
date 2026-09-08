package com.jk.explore.decorator;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * The trap: hardcodes insurance onto a product. This class and
 * {@link NaiveGiftWrappedProduct} share no common type -- each re-derives
 * its own cost and description logic independently.
 */
public final class NaiveInsuredProduct {

    private static final BigDecimal RATE = new BigDecimal("0.02");

    private final String name;
    private final BigDecimal price;

    public NaiveInsuredProduct(String name, BigDecimal price) {
        this.name = name;
        this.price = price;
    }

    public BigDecimal cost() {
        BigDecimal premium = price.multiply(RATE).setScale(2, RoundingMode.HALF_UP);
        return price.add(premium);
    }

    public String description() {
        return name + ", insured";
    }
}
