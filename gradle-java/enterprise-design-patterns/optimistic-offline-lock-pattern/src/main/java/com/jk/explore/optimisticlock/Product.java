package com.jk.explore.optimisticlock;

public record Product(String sku, long pricePence, int stock) {

    public Product withPrice(long pence) {
        return new Product(sku, pence, stock);
    }

    public Product withStock(int stock) {
        return new Product(sku, pricePence, stock);
    }
}
