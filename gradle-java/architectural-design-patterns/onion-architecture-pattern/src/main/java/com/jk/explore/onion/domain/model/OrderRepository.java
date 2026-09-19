package com.jk.explore.onion.domain.model;

import java.util.Optional;

/** The idea of storage, owned by the inside. The outside supplies the real thing. */
public interface OrderRepository {

    void save(Order order);

    Optional<Order> find(String id);
}
