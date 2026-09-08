package com.jk.explore.decorator;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * The trap: a third class for the combination of both features, duplicating
 * both fee calculations yet again. A third feature (express handling) would
 * require four more classes just to cover every combination with the two
 * that already exist.
 */
public final class NaiveGiftWrappedInsuredProduct {

    private static final BigDecimal GIFT_WRAP_FEE = new BigDecimal("3.50");
    private static final BigDecimal RATE = new BigDecimal("0.02");

    private final String name;
    private final BigDecimal price;

    public NaiveGiftWrappedInsuredProduct(String name, BigDecimal price) {
        this.name = name;
        this.price = price;
    }

    public BigDecimal cost() {
        BigDecimal wrapped = price.add(GIFT_WRAP_FEE);
        BigDecimal premium = wrapped.multiply(RATE).setScale(2, RoundingMode.HALF_UP);
        return wrapped.add(premium);
    }

    public String description() {
        return name + ", gift-wrapped, insured";
    }
}
