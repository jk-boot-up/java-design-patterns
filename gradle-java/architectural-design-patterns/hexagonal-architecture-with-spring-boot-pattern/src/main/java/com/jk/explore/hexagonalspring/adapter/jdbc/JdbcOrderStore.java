package com.jk.explore.hexagonalspring.adapter.jdbc;

import com.jk.explore.hexagonalspring.core.domain.Order;
import com.jk.explore.hexagonalspring.core.port.OrderStore;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Component;

@Component
@ConditionalOnProperty(name = "orders.store", havingValue = "jdbc")
public class JdbcOrderStore implements OrderStore {

    private final JdbcClient jdbc;

    public JdbcOrderStore(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    @Override
    public void save(Order o) {
        jdbc.sql("INSERT INTO orders VALUES (?, ?, ?, ?, ?)")
                .param(o.id()).param(o.customer()).param(o.sku()).param(o.quantity()).param(o.totalPence()).update();
    }

    @Override
    public int count() {
        return jdbc.sql("SELECT COUNT(*) FROM orders").query(Integer.class).single();
    }
}
