package com.jk.explore.clean.entities;

/** Something the shop sells. The stock level lives with the store, not here. */
public record Product(String sku, String name, Money price) {
}
