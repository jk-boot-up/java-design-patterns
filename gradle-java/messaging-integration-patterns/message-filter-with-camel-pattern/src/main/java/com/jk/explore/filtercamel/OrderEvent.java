package com.jk.explore.filtercamel;

/**
 * "An order was placed": sent to every service that listens for orders. Written as a class with
 * getters so Camel's Simple language can read ${body.gift} and ${body.pence}.
 */
public final class OrderEvent {

    private final String orderId;
    private final boolean registered;
    private final long pence;
    private final boolean gift;

    public OrderEvent(String orderId, boolean registered, long pence, boolean gift) {
        this.orderId = orderId;
        this.registered = registered;
        this.pence = pence;
        this.gift = gift;
    }

    public String getOrderId() {
        return orderId;
    }

    public boolean isRegistered() {
        return registered;
    }

    public long getPence() {
        return pence;
    }

    public boolean isGift() {
        return gift;
    }

    @Override
    public String toString() {
        return orderId;
    }
}
