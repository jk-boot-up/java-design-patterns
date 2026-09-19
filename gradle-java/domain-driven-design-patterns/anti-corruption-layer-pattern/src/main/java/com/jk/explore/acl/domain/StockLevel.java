package com.jk.explore.acl.domain;

/** How the shop thinks about stock: a sku, a number, and a meaning. No codes, no strings pretending to be numbers. */
public record StockLevel(String sku, int available, Availability availability) {

    public boolean canBeBought() {
        return availability == Availability.IN_STOCK && available > 0;
    }
}
