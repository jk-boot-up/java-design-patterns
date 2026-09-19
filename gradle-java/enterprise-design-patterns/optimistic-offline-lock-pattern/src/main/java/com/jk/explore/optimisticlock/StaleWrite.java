package com.jk.explore.optimisticlock;

public class StaleWrite extends RuntimeException {
    public StaleWrite(String sku) {
        super(sku + " was changed by someone else since you read it");
    }
}
