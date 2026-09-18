package com.jk.explore.clean.adapters.gateway;

import com.jk.explore.clean.entities.Money;
import com.jk.explore.clean.entities.Product;
import com.jk.explore.clean.usecases.ProductRepository;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;

public class InMemoryProductRepository implements ProductRepository {

    private final Map<String, Product> products = new LinkedHashMap<>();
    private final Map<String, Integer> stock = new LinkedHashMap<>();

    public static InMemoryProductRepository seeded() {
        InMemoryProductRepository repo = new InMemoryProductRepository();
        repo.add(new Product("ESP-001", "Espresso Machine", Money.pounds(249, 0)), 4);
        repo.add(new Product("GRD-014", "Burr Grinder", Money.pounds(89, 50)), 2);
        repo.add(new Product("BNS-220", "Coffee Beans, 1kg", Money.pounds(22, 0)), 40);
        return repo;
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
