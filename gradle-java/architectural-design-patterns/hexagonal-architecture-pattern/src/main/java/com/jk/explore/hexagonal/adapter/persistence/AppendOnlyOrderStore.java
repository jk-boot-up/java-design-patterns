package com.jk.explore.hexagonal.adapter.persistence;

import com.jk.explore.hexagonal.core.domain.Order;
import com.jk.explore.hexagonal.core.port.OrderStore;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * <strong>This class is the driven-side half of the forced change.</strong>
 * A completely different storage strategy — an append-only list, read
 * backwards — swapped in for {@link InMemoryOrderStore} with no change to
 * anything in {@code core}, because both classes implement the same port and
 * the core only ever names the port.
 */
public class AppendOnlyOrderStore implements OrderStore {

    private final List<Order> log = new ArrayList<>();

    @Override
    public void save(Order order) {
        log.add(order);
    }

    @Override
    public Optional<Order> find(String orderId) {
        for (int i = log.size() - 1; i >= 0; i--) {
            if (log.get(i).id().equals(orderId)) {
                return Optional.of(log.get(i));
            }
        }
        return Optional.empty();
    }

    @Override
    public List<Order> all() {
        List<Order> newest = new ArrayList<>();
        for (Order order : log) {
            if (find(order.id()).filter(found -> found == order).isPresent()) {
                newest.add(order);
            }
        }
        return newest;
    }

    @Override
    public int count() {
        return all().size();
    }

    @Override
    public String describe() {
        return "an append-only log, read backwards";
    }
}
