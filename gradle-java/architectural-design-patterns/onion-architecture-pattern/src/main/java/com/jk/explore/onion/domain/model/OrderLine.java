package com.jk.explore.onion.domain.model;

public record OrderLine(String sku, int quantity, long unitCents) {

    public long cents() {
        return quantity * unitCents;
    }
}
