package com.jk.explore.layered.domain;

/** Something the shop sells. The stock level lives with the store, not here. */
public record Product(String sku, String name, Money price) {
}
