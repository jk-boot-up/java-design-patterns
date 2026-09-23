package com.jk.explore.splitteraggregatorcamel;

/**
 * One piece of a split order after its warehouse has picked and priced it. It carries the order number it
 * belongs to and its own place in the order, and those two facts are the whole reason it can be put back.
 */
public record Shipment(String orderId, int index, int of, String warehouse, String contents, int pence) {

    public String describe() {
        return contents + " from " + warehouse;
    }
}
