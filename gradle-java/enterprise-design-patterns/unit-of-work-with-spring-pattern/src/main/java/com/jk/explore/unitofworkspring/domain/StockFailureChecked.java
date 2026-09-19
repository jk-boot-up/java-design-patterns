package com.jk.explore.unitofworkspring.domain;

/** The same failure as a checked exception. Spring does not roll back on these by default. */
public class StockFailureChecked extends Exception {

    public StockFailureChecked(int productId) {
        super("the stock update for product " + productId + " was rejected");
    }
}
