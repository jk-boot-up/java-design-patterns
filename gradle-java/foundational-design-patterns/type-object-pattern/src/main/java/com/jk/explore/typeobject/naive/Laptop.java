package com.jk.explore.typeobject.naive;

public class Laptop extends KindProduct {

    public Laptop(long priceCents) {
        super(priceCents);
    }

    @Override
    protected int taxPercent() {
        return 20;
    }

    @Override
    protected int shippingCents() {
        return 0;
    }
}
