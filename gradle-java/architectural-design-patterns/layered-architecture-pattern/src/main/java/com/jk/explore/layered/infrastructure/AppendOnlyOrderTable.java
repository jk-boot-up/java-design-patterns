package com.jk.explore.layered.infrastructure;

import com.jk.explore.layered.domain.Order;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * <strong>This class is the forced change.</strong>
 *
 * <p>It stores orders completely differently from {@link InMemoryOrderTable}:
 * an append-only list, never updated in place, with a read walking backwards to
 * find the newest version of a given id. That is roughly how a log-structured
 * store behaves, and it is about as far from "a map keyed by id" as a storage
 * decision gets while still being one page of code.
 *
 * <p>The point of the exercise is what happened to everything else. Adding this
 * file and pointing the composition root at it replaced the entire storage
 * layer, and not one class in the domain, application or presentation layers
 * was opened. The demo prints that count, and the number — not the adjective —
 * is the argument for layering.
 */
public class AppendOnlyOrderTable implements OrderTable {

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
