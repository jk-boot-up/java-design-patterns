package com.jk.explore.typeobject.naive;

public class Grocery extends KindProduct {

    public Grocery(long priceCents) {
        super(priceCents);
    }

    @Override
    protected int taxPercent() {
        return 5;
    }

    @Override
    protected int shippingCents() {
        return 200;
    }
}
