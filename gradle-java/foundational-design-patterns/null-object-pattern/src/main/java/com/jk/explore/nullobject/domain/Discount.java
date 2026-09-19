package com.jk.explore.nullobject.domain;

/** What a discount does to a price, in pence. */
public interface Discount {

    long apply(long pricePence);

    String name();
}
