package com.jk.explore.nullobject.domain;

/** Twenty-five per cent off for staff. */
public final class StaffDiscount implements Discount {

    @Override
    public long apply(long pricePence) {
        return pricePence * 75 / 100;
    }

    @Override
    public String name() {
        return "staff 25%";
    }
}
