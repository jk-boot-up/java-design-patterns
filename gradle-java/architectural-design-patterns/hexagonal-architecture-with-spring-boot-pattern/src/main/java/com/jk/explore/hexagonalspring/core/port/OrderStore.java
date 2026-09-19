package com.jk.explore.hexagonalspring.core.port;

import com.jk.explore.hexagonalspring.core.domain.Order;

/** Driven port: where orders are kept. Declared by the core, implemented outside it. */
public interface OrderStore {
    void save(Order order);

    int count();
}
