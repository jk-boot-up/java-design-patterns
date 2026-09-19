package com.jk.explore.futurepromise.domain;

/**
 * One slow catalogue lookup — price, stock or a review score — for a
 * product's SKU. Each of the three the product page needs genuinely takes
 * time and does not depend on either of the other two.
 */
@FunctionalInterface
public interface Lookup<T> {

    T fetch(String sku);
}
