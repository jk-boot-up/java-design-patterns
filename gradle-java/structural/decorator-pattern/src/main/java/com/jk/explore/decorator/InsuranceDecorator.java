package com.jk.explore.decorator;

import java.math.BigDecimal;
import java.math.RoundingMode;

public final class InsuranceDecorator extends ProductDecorator {

    private static final BigDecimal RATE = new BigDecimal("0.02");

    public InsuranceDecorator(PricedItem wrapped) {
        super(wrapped);
    }

    @Override
    public BigDecimal cost() {
        BigDecimal base = wrapped.cost();
        BigDecimal premium = base.multiply(RATE).setScale(2, RoundingMode.HALF_UP);
        return base.add(premium);
    }

    @Override
    public String description() {
        return wrapped.description() + ", insured";
    }
}
