package com.jk.explore.layeredspring.infrastructure;

import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Repository;

@Repository
public class ProductRepository {

    private final JdbcClient jdbc;

    public ProductRepository(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    public long priceOf(String sku) {
        return jdbc.sql("SELECT price_pence FROM products WHERE sku = ?").param(sku).query(Long.class).single();
    }

    public long costOf(String sku) {
        return jdbc.sql("SELECT cost_pence FROM products WHERE sku = ?").param(sku).query(Long.class).single();
    }

    public int stockOf(String sku) {
        return jdbc.sql("SELECT stock FROM products WHERE sku = ?").param(sku).query(Integer.class).single();
    }

    /** @return false when there is not enough stock; nothing is changed then */
    public boolean reserve(String sku, int quantity) {
        return jdbc.sql("UPDATE products SET stock = stock - ? WHERE sku = ? AND stock >= ?")
                .param(quantity).param(sku).param(quantity).update() == 1;
    }
}
