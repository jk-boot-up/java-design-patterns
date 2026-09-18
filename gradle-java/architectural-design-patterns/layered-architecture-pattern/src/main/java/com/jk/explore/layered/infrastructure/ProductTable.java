package com.jk.explore.layered.infrastructure;

import com.jk.explore.layered.domain.Money;
import com.jk.explore.layered.domain.Product;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;

/**
 * The catalogue as it is actually stored: a row per product, and a stock count
 * beside it.
 *
 * <p>Seeded with the three products from the category's shared feature
 * specification, so that all five projects in this category print recognisably
 * the same run.
 */
public class ProductTable {

    private final Map<String, Product> products = new LinkedHashMap<>();
    private final Map<String, Integer> stock = new LinkedHashMap<>();

    public static ProductTable seeded() {
        ProductTable table = new ProductTable();
        table.add(new Product("ESP-001", "Espresso Machine", Money.pounds(249, 0)), 4);
        table.add(new Product("GRD-014", "Burr Grinder", Money.pounds(89, 50)), 2);
        table.add(new Product("BNS-220", "Coffee Beans, 1kg", Money.pounds(22, 0)), 40);
        return table;
    }

    public void add(Product product, int quantity) {
        products.put(product.sku(), product);
        stock.put(product.sku(), quantity);
    }

    public Optional<Product> find(String sku) {
        return Optional.ofNullable(products.get(sku));
    }

    public int stockOf(String sku) {
        return stock.getOrDefault(sku, 0);
    }

    public void reduceStock(String sku, int quantity) {
        stock.put(sku, stockOf(sku) - quantity);
    }
}
