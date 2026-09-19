package com.jk.explore.delegation.naive;

public class PremiumOrder extends PlainOrder {

    public PremiumOrder(long subtotalCents) {
        super(subtotalCents);
    }

    @Override
    public long total() {
        return super.total() - super.total() / 10;
    }
}
