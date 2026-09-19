package com.jk.explore.registryspring.domain;

import org.springframework.stereotype.Component;

/** Ten per cent off. */
@Component
public final class LoyaltyPolicy implements DiscountPolicy {

    @Override
    public long apply(long pricePence) {
        return pricePence * 90 / 100;
    }
}
