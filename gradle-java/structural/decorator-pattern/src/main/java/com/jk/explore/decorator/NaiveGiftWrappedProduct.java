package com.jk.explore.decorator;

import java.math.BigDecimal;

/**
 * The trap: hardcodes gift-wrapping onto a product. Adding insurance to this
 * exact combination means writing a whole new class, not reusing this one.
 */
public final class NaiveGiftWrappedProduct {

    private static final BigDecimal GIFT_WRAP_FEE = new BigDecimal("3.50");

    private final String name;
    private final BigDecimal price;

    public NaiveGiftWrappedProduct(String name, BigDecimal price) {
        this.name = name;
        this.price = price;
    }

    public BigDecimal cost() {
        return price.add(GIFT_WRAP_FEE);
    }

    public String description() {
        return name + ", gift-wrapped";
    }
}
