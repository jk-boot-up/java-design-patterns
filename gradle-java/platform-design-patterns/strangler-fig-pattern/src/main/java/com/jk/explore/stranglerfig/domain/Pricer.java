package com.jk.explore.stranglerfig.domain;

public interface Pricer {
    Pricing price(Order order);
}
