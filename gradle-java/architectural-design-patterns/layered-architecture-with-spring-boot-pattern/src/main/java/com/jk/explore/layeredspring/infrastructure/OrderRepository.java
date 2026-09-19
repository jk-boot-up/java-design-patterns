package com.jk.explore.layeredspring.infrastructure;

import com.jk.explore.layeredspring.domain.Order;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public class OrderRepository {

    private final JdbcClient jdbc;

    public OrderRepository(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    public void save(Order order) {
        jdbc.sql("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)")
                .param(order.id()).param(order.customer()).param(order.sku()).param(order.quantity())
                .param(order.totalPence()).param(order.costPence()).param(order.status()).update();
    }

    public Optional<Order> find(String id) {
        return jdbc.sql("SELECT id, customer, sku, quantity, total_pence, cost_pence, status FROM orders WHERE id = ?")
                .param(id)
                .query((rs, n) -> new Order(rs.getString(1), rs.getString(2), rs.getString(3), rs.getInt(4),
                        rs.getLong(5), rs.getLong(6), rs.getString(7)))
                .optional();
    }

    public int count() {
        return jdbc.sql("SELECT COUNT(*) FROM orders").query(Integer.class).single();
    }
}
