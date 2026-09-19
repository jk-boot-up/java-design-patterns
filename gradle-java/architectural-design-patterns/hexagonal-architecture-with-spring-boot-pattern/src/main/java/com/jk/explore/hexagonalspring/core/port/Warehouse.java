package com.jk.explore.hexagonalspring.core.port;

/** Driven port: what the shop sells, at what price, and how many are left. */
public interface Warehouse {
    long priceOf(String sku);

    /** @return false, changing nothing, when there is not enough stock */
    boolean reserve(String sku, int quantity);

    int stockOf(String sku);
}
