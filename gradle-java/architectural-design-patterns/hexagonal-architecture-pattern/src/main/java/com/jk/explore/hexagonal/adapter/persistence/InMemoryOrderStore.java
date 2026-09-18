package com.jk.explore.hexagonal.adapter.persistence;

import com.jk.explore.hexagonal.core.domain.Order;
import com.jk.explore.hexagonal.core.port.OrderStore;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * A driven adapter: it sits on the outside and <em>implements</em> a port the
 * core defined, rather than the core naming this class. Orders in a map,
 * keyed by id.
 */
public class InMemoryOrderStore implements OrderStore {

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
