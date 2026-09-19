package com.jk.explore.mvcspring;

import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

/** Holds orders in memory. ORD-000001 is Ada's, seeded: a machine and two bags of beans. */
@Repository
public class OrderStore {

    private static final Map<String, Long> PRICES = Map.of("ESP-001", 30000L, "BNS-220", 1250L);

    private final Map<String, Order> orders = new ConcurrentHashMap<>();
    private final AtomicInteger sequence = new AtomicInteger();

    public OrderStore() {
        String id = nextId();
        orders.put(id, new Order(id, "ada", List.of(new Line("ESP-001", 1, 30000), new Line("BNS-220", 2, 1250))));
    }

    private String nextId() {
        return String.format("ORD-%06d", sequence.incrementAndGet());
    }

    public Order place(String customer, String sku, int quantity) {
        String id = nextId();
        Order order = new Order(id, customer, List.of(new Line(sku, quantity, PRICES.getOrDefault(sku, 0L))));
        orders.put(id, order);
        return order;
    }

    public Optional<Order> find(String id) {
        return Optional.ofNullable(orders.get(id));
    }
}
