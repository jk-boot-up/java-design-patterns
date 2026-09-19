package com.jk.explore.nullobject.domain;

/** Ten per cent off for loyal customers. */
public final class LoyaltyDiscount implements Discount {

    @Override
    public long apply(long pricePence) {
        return pricePence * 90 / 100;
    }

    @Override
    public String name() {
        return "loyalty 10%";
    }
}
