package com.jk.explore.bridge;

import java.util.Objects;

/** A refined Abstraction. Composes its own subject and body only. */
public final class ShippingUpdateNotification extends Notification {

    private final String orderId;
    private final String status;

    public ShippingUpdateNotification(MessageChannel channel, String orderId, String status) {
        super(channel);
        this.orderId = Objects.requireNonNull(orderId);
        this.status = Objects.requireNonNull(status);
    }

    @Override
    protected String subject() {
        return "Shipping update for order " + orderId;
    }

    @Override
    protected String body() {
        return "Order " + orderId + " is now: " + status;
    }
}
