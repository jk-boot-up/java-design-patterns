package com.jk.explore.hexagonalspring.core.domain;

public class OutOfStock extends RuntimeException {
    public OutOfStock(String sku) {
        super("not enough " + sku + " in stock");
    }
}
