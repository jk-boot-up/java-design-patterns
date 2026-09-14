package com.jk.explore.saga;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Orders. Creates the order, and cancels it.
 *
 * Cancelling is not deleting. The order stays, with its state set to CANCELLED, because the
 * customer saw it, the finance team will report on it, and pretending it never happened
 * would leave everybody with a different history of the same afternoon.
 */
public final class OrderService {

    public static final long LATENCY_MILLIS = 20;

    /** An order's state. There is no state called "nearly". */
    public enum State { CONFIRMED, CANCELLED }

    private final Map<String, State> orders = new LinkedHashMap<>();
    private final RemoteCall<SagaContext, String> create;
    private final RemoteCall<String, String> cancel;

    public OrderService(SimulatedClock clock, CallLog log) {
        this.create = new RemoteCall<>("Orders", LATENCY_MILLIS, this::doCreate, clock, log);
        this.cancel = new RemoteCall<>("Orders", LATENCY_MILLIS, this::doCancel, clock, log);
    }

    public String create(SagaContext context) {
        return create.invoke(context);
    }

    public String cancel(String orderRef) {
        return cancel.invoke(orderRef);
    }

    public void failNextCreate(int count) {
        create.failNext(count);
    }

    public void failNextCancel(int count) {
        cancel.failNext(count);
    }

    public State stateOf(String orderRef) {
        return orders.get(orderRef);
    }

    public long countIn(State state) {
        return orders.values().stream().filter(s -> s == state).count();
    }

    private String doCreate(SagaContext context) {
        orders.put(context.orderId(), State.CONFIRMED);
        return context.orderId();
    }

    private String doCancel(String orderRef) {
        orders.put(orderRef, State.CANCELLED);
        return "cancelled " + orderRef;
    }
}
