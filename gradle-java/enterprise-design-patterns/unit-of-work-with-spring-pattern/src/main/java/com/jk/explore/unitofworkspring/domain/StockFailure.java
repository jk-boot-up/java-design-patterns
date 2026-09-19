package com.jk.explore.unitofworkspring.domain;

/** The third stock update fails. An unchecked exception: Spring rolls back on these by default. */
public class StockFailure extends RuntimeException {

    public StockFailure(int productId) {
        super("the stock update for product " + productId + " was rejected");
    }
}
