package com.jk.explore.hexagonalspring.adapter.jdbc;

import com.jk.explore.hexagonalspring.core.port.Warehouse;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Component;

@Component
@ConditionalOnProperty(name = "orders.store", havingValue = "jdbc")
public class JdbcWarehouse implements Warehouse {

    private final JdbcClient jdbc;

    public JdbcWarehouse(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    @Override
    public long priceOf(String sku) {
        return jdbc.sql("SELECT price_pence FROM stock WHERE sku = ?").param(sku).query(Long.class).optional().orElse(0L);
    }

    @Override
    public boolean reserve(String sku, int quantity) {
        return jdbc.sql("UPDATE stock SET on_hand = on_hand - ? WHERE sku = ? AND on_hand >= ?")
                .param(quantity).param(sku).param(quantity).update() == 1;
    }

    @Override
    public int stockOf(String sku) {
        return jdbc.sql("SELECT on_hand FROM stock WHERE sku = ?").param(sku).query(Integer.class).optional().orElse(0);
    }
}
