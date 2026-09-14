package com.jk.explore.cqrs;

/** The shelf could not cover what somebody tried to buy. */
public class OutOfStockException extends RuntimeException {

    public OutOfStockException(String sku, int wanted, int available) {
        super("cannot reserve " + wanted + " of " + sku + ", only " + available + " left");
    }
}
