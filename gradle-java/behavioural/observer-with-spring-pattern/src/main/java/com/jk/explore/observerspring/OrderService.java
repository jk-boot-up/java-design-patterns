package com.jk.explore.observerspring;

import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;

import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/**
 * The subject. It holds an event publisher and nothing else: no list of listeners, and no
 * field named after any of them.
 */
@Service
public class OrderService {

    private final ApplicationEventPublisher publisher;
    private final Set<String> shipped = ConcurrentHashMap.newKeySet();

    public OrderService(ApplicationEventPublisher publisher) {
        this.publisher = publisher;
    }

    public void ship(String orderId) {
        shipped.add(orderId);
        publisher.publishEvent(new OrderStatusChanged(orderId, "PAID", "SHIPPED"));
    }

    public void cancel(String orderId) {
        publisher.publishEvent(new OrderStatusChanged(orderId, "PAID", "CANCELLED"));
    }

    public void refund(String orderId) {
        publisher.publishEvent(new OrderRefunded(orderId));
    }

    public boolean isShipped(String orderId) {
        return shipped.contains(orderId);
    }
}
