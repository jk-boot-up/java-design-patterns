package com.jk.explore.onion.domain.model;

import java.util.List;

/** The centre of the onion. It knows nothing about storage, screens or frameworks. */
public class Order {

    private final String id;
    private final List<OrderLine> lines;
    private long discountCents;

    public Order(String id, List<OrderLine> lines) {
        if (lines.isEmpty()) {
            throw new IllegalArgumentException("an order needs at least one line");
        }
        this.id = id;
        this.lines = List.copyOf(lines);
    }

    public String id() {
        return id;
    }

    public List<OrderLine> lines() {
        return lines;
    }

    public long subtotalCents() {
        return lines.stream().mapToLong(OrderLine::cents).sum();
    }

    public void applyDiscount(long cents) {
        this.discountCents = cents;
    }

    public long totalCents() {
        return subtotalCents() - discountCents;
    }
}
