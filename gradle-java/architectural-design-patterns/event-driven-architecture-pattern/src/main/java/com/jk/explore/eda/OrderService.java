package com.jk.explore.eda;

/** Accepts an order and tells the log. It does not know who reads the log. */
public class OrderService {

    private final EventLog log;

    public OrderService(EventLog log) {
        this.log = log;
    }

    public int place(String orderId) {
        return log.append("OrderPlaced", orderId);
    }
}
