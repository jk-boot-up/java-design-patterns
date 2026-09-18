package com.jk.explore.cleanspring.usecases;

import com.jk.explore.cleanspring.entities.Product;

import java.util.Optional;

public interface ProductRepository {

    Optional<Product> find(String sku);

    int stockOf(String sku);

    void reduceStock(String sku, int quantity);
}
