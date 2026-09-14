package com.jk.explore.apicomposition;

import java.util.List;
import java.util.Map;

/** Orders. The fastest of the three, and the one the page cannot do without. */
public final class OrderService {

    public static final long LATENCY_MILLIS = 30;

    private static final Map<String, Order> ORDERS = Map.of(
            "ord-3001", new Order("ord-3001", "cust-7", List.of(
                    new Order.Line("SKU-KETTLE", 1, Money.pence(3499)),
                    new Order.Line("SKU-MUG", 4, Money.pence(899)))));

    private final RemoteCall<String, Order> fetch;

    public OrderService(SimulatedClock clock, CallLog log) {
        this.fetch = new RemoteCall<>("Orders", LATENCY_MILLIS,
                orderId -> lookUp(orderId), clock, log);
    }

    public Order fetch(String orderId) {
        return fetch.invoke(orderId);
    }

    /** Scripts the next {@code count} calls to fail. */
    public void goDown(int count) {
        fetch.failNext(count);
    }

    public int callsReceived() {
        return fetch.invocations();
    }

    private static Order lookUp(String orderId) {
        Order order = ORDERS.get(orderId);
        if (order == null) {
            throw new IllegalArgumentException("no such order: " + orderId);
        }
        return order;
    }
}
