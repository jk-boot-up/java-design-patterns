package com.jk.explore.domainevent.domain;

import java.util.ArrayList;
import java.util.List;

/**
 * An order that says what happened to it. It does not call anyone. Each change records an event, and
 * whoever saves the order collects the events afterwards.
 */
public final class Order {

    public enum Status { DRAFT, PLACED, CANCELLED }

    private final String id;
    private final String customerId;
    private final long totalPence;
    private Status status = Status.DRAFT;
    private final List<DomainEvent> pending = new ArrayList<>();

    public Order(String id, String customerId, long totalPence) {
        this.id = id;
        this.customerId = customerId;
        this.totalPence = totalPence;
    }

    public String id() {
        return id;
    }

    public Status status() {
        return status;
    }

    public void place() {
        if (status != Status.DRAFT) {
            throw new IllegalStateException("only a draft can be placed");
        }
        status = Status.PLACED;
        pending.add(new OrderPlaced(id, customerId, totalPence));
    }

    public void cancel(String reason) {
        if (status != Status.PLACED) {
            throw new IllegalStateException("only a placed order can be cancelled");
        }
        status = Status.CANCELLED;
        pending.add(new OrderCancelled(id, reason));
    }

    /** Hands over the events recorded since the last call, in the order they happened, and forgets them. */
    public List<DomainEvent> pullEvents() {
        List<DomainEvent> events = List.copyOf(pending);
        pending.clear();
        return events;
    }
}
