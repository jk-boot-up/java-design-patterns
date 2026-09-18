package com.jk.explore.hexagonal.core.port;

import com.jk.explore.hexagonal.core.domain.Product;

import java.util.Optional;

/** What the core needs to know about the catalogue — nothing about how it is stored. */
public interface ProductCatalog {

    Optional<Product> find(String sku);

    int stockOf(String sku);

    void reduceStock(String sku, int quantity);
}
