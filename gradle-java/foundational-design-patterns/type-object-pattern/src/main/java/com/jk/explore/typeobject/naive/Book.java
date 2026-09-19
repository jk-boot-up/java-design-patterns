package com.jk.explore.typeobject.naive;

public class Book extends KindProduct {

    public Book(long priceCents) {
        super(priceCents);
    }

    @Override
    protected int taxPercent() {
        return 0;
    }

    @Override
    protected int shippingCents() {
        return 300;
    }
}
