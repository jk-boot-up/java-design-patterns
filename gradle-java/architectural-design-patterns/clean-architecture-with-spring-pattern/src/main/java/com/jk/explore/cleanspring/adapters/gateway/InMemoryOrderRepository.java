package com.jk.explore.cleanspring.adapters.gateway;

import com.jk.explore.cleanspring.entities.Order;
import com.jk.explore.cleanspring.usecases.OrderRepository;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/** A gateway: it implements a use-case boundary. Orders in a map, keyed by id. */
public class InMemoryOrderRepository implements OrderRepository {

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
