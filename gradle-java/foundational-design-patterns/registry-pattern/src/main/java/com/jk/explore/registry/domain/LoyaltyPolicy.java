package com.jk.explore.registry.domain;

/** Ten per cent off. */
public final class LoyaltyPolicy implements DiscountPolicy {

    @Override
    public long apply(long pricePence) {
        return pricePence * 90 / 100;
    }
}
