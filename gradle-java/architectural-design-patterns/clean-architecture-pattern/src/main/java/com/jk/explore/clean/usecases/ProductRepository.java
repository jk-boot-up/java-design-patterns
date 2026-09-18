package com.jk.explore.clean.usecases;

import com.jk.explore.clean.entities.Product;

import java.util.Optional;

public interface ProductRepository {

    Optional<Product> find(String sku);

    int stockOf(String sku);

    void reduceStock(String sku, int quantity);
}
