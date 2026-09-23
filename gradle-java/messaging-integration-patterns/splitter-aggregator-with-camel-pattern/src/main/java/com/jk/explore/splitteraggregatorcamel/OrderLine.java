package com.jk.explore.splitteraggregatorcamel;

/**
 * One line of a customer's basket: how many of which product, what one of them costs in pence, and which
 * warehouse holds it. The warehouse is what decides where this line has to be sent.
 */
public record OrderLine(String sku, int quantity, int unitPence, String warehouse) {

    public int linePence() {
        return quantity * unitPence;
    }

    public String describe() {
        return quantity + " x " + sku;
    }
}
