package com.jk.explore.saga;

/** The shelf could not cover the basket. A perfectly ordinary reason to stop. */
public class OutOfStockException extends RuntimeException {

    public OutOfStockException(String sku, int wanted, int available) {
        super("cannot reserve " + wanted + " of " + sku + ", only " + available + " left");
    }
}
