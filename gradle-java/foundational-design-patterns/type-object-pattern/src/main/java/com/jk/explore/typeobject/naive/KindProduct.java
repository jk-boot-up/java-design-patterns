package com.jk.explore.typeobject.naive;

/** The version with a subclass for each kind. */
public abstract class KindProduct {

    private final long priceCents;

    protected KindProduct(long priceCents) {
        this.priceCents = priceCents;
    }

    protected abstract int taxPercent();

    protected abstract int shippingCents();

    public long totalCents() {
        return priceCents + priceCents * taxPercent() / 100 + shippingCents();
    }
}
