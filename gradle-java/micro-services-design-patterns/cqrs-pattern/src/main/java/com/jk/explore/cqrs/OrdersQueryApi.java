package com.jk.explore.cqrs;

import java.util.List;

/**
 * The write side's orders, over the network, as another service would see them.
 *
 * This exists so that the composing order history page has something to call. It is the
 * write model being read, which is exactly the thing CQRS says to stop doing on a hot
 * page — and, to be fair to it, exactly the right thing to do on a page nobody looks at.
 */
public final class OrdersQueryApi {

    public static final long LATENCY_MILLIS = 30;

    private final RemoteCall<String, List<Order>> ordersFor;

    public OrdersQueryApi(OrderWriteService writeSide, SimulatedClock clock, CallLog log) {
        this.ordersFor = new RemoteCall<>("Orders", LATENCY_MILLIS,
                customerId -> writeSide.allOrders().stream()
                        .filter(order -> order.customerId().equals(customerId))
                        .toList(),
                clock, log);
    }

    public List<Order> ordersFor(String customerId) {
        return ordersFor.invoke(customerId);
    }

    public void goDown(int count) {
        ordersFor.failNext(count);
    }

    public int callsReceived() {
        return ordersFor.invocations();
    }
}
