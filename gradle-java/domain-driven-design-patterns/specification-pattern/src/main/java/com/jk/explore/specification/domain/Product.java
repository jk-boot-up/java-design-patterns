package com.jk.explore.specification.domain;

public record Product(String sku, String category, long pricePence, boolean inStock, boolean onSale, boolean discontinued) {
}
