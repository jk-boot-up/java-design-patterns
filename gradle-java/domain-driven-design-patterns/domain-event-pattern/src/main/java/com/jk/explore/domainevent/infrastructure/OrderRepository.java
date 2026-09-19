package com.jk.explore.domainevent.infrastructure;

import com.jk.explore.domainevent.domain.DomainEvent;
import com.jk.explore.domainevent.domain.Order;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Saves an order and, in the same step, keeps the events it recorded. A separate relay delivers them to
 * the handlers. A delivery that fails stays pending and is retried on the next relay. Saving the events
 * with the order is what stops an event being lost if the process stops between the two.
 */
public class OrderRepository {

    private record Pending(DomainEvent event, Set<String> deliveredTo) {
    }

    private final Map<String, Order> orders = new LinkedHashMap<>();
    private final List<Pending> outbox = new ArrayList<>();
    private final List<EventHandler> handlers;

    public OrderRepository(List<EventHandler> handlers) {
        this.handlers = handlers;
    }

    public synchronized void save(Order order) {
        orders.put(order.id(), order);
        for (DomainEvent event : order.pullEvents()) {
            outbox.add(new Pending(event, new HashSet<>()));
        }
    }

    public synchronized int pending() {
        return (int) outbox.stream().filter(p -> p.deliveredTo().size() < handlers.size()).count();
    }

    /** Offers every undelivered event to every handler that has not had it yet. Returns the failures. */
    public synchronized List<String> relay() {
        List<String> failures = new ArrayList<>();
        for (Pending p : outbox) {
            for (EventHandler handler : handlers) {
                if (p.deliveredTo().contains(handler.name())) {
                    continue;
                }
                try {
                    handler.handle(p.event());
                    p.deliveredTo().add(handler.name());
                } catch (RuntimeException e) {
                    failures.add(handler.name() + " failed on " + p.event().getClass().getSimpleName() + " for " + p.event().orderId() + ": " + e.getMessage());
                }
            }
        }
        return failures;
    }
}
