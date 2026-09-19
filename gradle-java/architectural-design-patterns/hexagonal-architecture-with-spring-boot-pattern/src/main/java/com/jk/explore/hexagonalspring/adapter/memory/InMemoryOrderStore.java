package com.jk.explore.hexagonalspring.adapter.memory;

import com.jk.explore.hexagonalspring.core.domain.Order;
import com.jk.explore.hexagonalspring.core.port.OrderStore;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Component
@ConditionalOnProperty(name = "orders.store", havingValue = "memory", matchIfMissing = true)
public class InMemoryOrderStore implements OrderStore {

    private final List<Order> orders = Collections.synchronizedList(new ArrayList<>());

    @Override
    public void save(Order order) {
        orders.add(order);
    }

    @Override
    public int count() {
        return orders.size();
    }
}
