package com.jk.explore.stranglerfig.domain;

public record Line(String sku, int quantity, long unitPence) {

    public long linePence() {
        return quantity * unitPence;
    }
}
