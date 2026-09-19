package com.jk.explore.diwithspring.domain;

/** How a price is reduced. One of the three collaborators every checkout in this category needs. */
public interface DiscountPolicy {

    long apply(long pricePence);
}
