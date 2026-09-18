package com.jk.explore.hexagonal.adapter.persistence;

import com.jk.explore.hexagonal.core.domain.Money;
import com.jk.explore.hexagonal.core.domain.Product;
import com.jk.explore.hexagonal.core.port.ProductCatalog;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;

/**
 * Seeded with the three products from the category's shared feature
 * specification, so all five projects print recognisably the same run.
 */
public class InMemoryProductCatalog implements ProductCatalog {

    private final Map<String, Product> products = new LinkedHashMap<>();
    private final Map<String, Integer> stock = new LinkedHashMap<>();

    public static InMemoryProductCatalog seeded() {
        InMemoryProductCatalog catalog = new InMemoryProductCatalog();
        catalog.add(new Product("ESP-001", "Espresso Machine", Money.pounds(249, 0)), 4);
        catalog.add(new Product("GRD-014", "Burr Grinder", Money.pounds(89, 50)), 2);
        catalog.add(new Product("BNS-220", "Coffee Beans, 1kg", Money.pounds(22, 0)), 40);
        return catalog;
    }

    private void add(Product product, int quantity) {
        products.put(product.sku(), product);
        stock.put(product.sku(), quantity);
    }

    @Override
    public Optional<Product> find(String sku) {
        return Optional.ofNullable(products.get(sku));
    }

    @Override
    public int stockOf(String sku) {
        return stock.getOrDefault(sku, 0);
    }

    @Override
    public void reduceStock(String sku, int quantity) {
        stock.put(sku, stockOf(sku) - quantity);
    }
}
