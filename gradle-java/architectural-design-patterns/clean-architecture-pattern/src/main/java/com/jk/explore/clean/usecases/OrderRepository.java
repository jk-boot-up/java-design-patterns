package com.jk.explore.clean.usecases;

import com.jk.explore.clean.entities.Order;

import java.util.List;
import java.util.Optional;

/**
 * Declared here, in the use case layer — not in {@code entities}, because
 * "where orders are kept" is not a fact about an order, and not in
 * {@code adapters}, because the use case must not wait on an adapter to
 * know what it needs. A gateway in the outer circle implements this;
 * nothing in here or in {@code entities} knows which one.
 */
public interface OrderRepository {

    void save(Order order);

    Optional<Order> find(String orderId);

    List<Order> all();

    int count();

    String describe();
}
