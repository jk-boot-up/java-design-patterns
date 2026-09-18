package com.jk.explore.mvc.infrastructure;

import com.jk.explore.mvc.domain.Order;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Orders in a map, keyed by id. The obvious implementation, and the one the
 * project starts with.
 */
public class InMemoryOrderTable implements OrderTable {

    private final Map<String, Order> rows = new LinkedHashMap<>();

    @Override
    public void save(Order order) {
        rows.put(order.id(), order);
    }

    @Override
    public Optional<Order> find(String orderId) {
        return Optional.ofNullable(rows.get(orderId));
    }

    @Override
    public List<Order> all() {
        return new ArrayList<>(rows.values());
    }

    @Override
    public int count() {
        return rows.size();
    }

    @Override
    public String describe() {
        return "a map keyed by order id";
    }
}
