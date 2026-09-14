package com.jk.explore.databaseperservice;

import java.util.List;

/** The Orders service. Owns the order tables, and answers questions about orders. */
public final class OrderService {

    /** How long a call to this service takes from another service. */
    public static final long LATENCY_MILLIS = 10;

    private final OrderDatabase database;
    private final SimulatedClock clock;
    private final CallLog log;
    private int callsReceived;

    public OrderService(OrderDatabase database, SimulatedClock clock, CallLog log) {
        this.database = database;
        this.clock = clock;
        this.log = log;
    }

    /** Every order a customer has placed. Skus, quantities, and no product names. */
    public List<Order> ordersFor(String customerId) {
        callsReceived++;
        long startedAt = clock.millis();
        clock.advance(LATENCY_MILLIS);
        List<Order> orders = database.ordersFor("Orders", customerId);
        log.record(startedAt, clock.millis(), "Orders", "OK", orders.size() + " order(s)");
        return orders;
    }

    public int callsReceived() {
        return callsReceived;
    }
}
