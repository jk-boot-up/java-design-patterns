package com.jk.explore.cacheasideredis;

/** One product on the shop's shelves, and its price in pence. */
public record Product(String sku, long pricePence) {
}
