package com.jk.explore.onion.infrastructure;

import com.jk.explore.onion.domain.model.Order;
import com.jk.explore.onion.domain.model.OrderRepository;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

public class InMemoryOrderRepository implements OrderRepository {

    private final Map<String, Order> orders = new HashMap<>();

    @Override
    public void save(Order order) {
        orders.put(order.id(), order);
    }

    @Override
    public Optional<Order> find(String id) {
        return Optional.ofNullable(orders.get(id));
    }
}
