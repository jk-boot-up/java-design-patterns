package com.jk.explore.decorator;

import java.math.BigDecimal;

public final class GiftWrapDecorator extends ProductDecorator {

    private static final BigDecimal FEE = new BigDecimal("3.50");

    public GiftWrapDecorator(PricedItem wrapped) {
        super(wrapped);
    }

    @Override
    public BigDecimal cost() {
        return wrapped.cost().add(FEE);
    }

    @Override
    public String description() {
        return wrapped.description() + ", gift-wrapped";
    }
}
