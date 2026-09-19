package com.jk.explore.stranglerfig.domain;

public interface StockKeeper {
    boolean reserve(Order order);

    int onHand(String sku);
}
