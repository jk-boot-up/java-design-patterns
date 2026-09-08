package com.jk.explore.decorator;

import java.math.BigDecimal;

public final class ExpressHandlingDecorator extends ProductDecorator {

    private static final BigDecimal FEE = new BigDecimal("9.99");

    public ExpressHandlingDecorator(PricedItem wrapped) {
        super(wrapped);
    }

    @Override
    public BigDecimal cost() {
        return wrapped.cost().add(FEE);
    }

    @Override
    public String description() {
        return wrapped.description() + ", express handling";
    }
}
