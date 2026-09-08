package com.jk.explore.bridge;

import java.math.BigDecimal;
import java.util.Objects;

/** A refined Abstraction. Composes its own subject and body only. */
public final class OrderConfirmationNotification extends Notification {

    private final String orderId;
    private final BigDecimal total;

    public OrderConfirmationNotification(MessageChannel channel, String orderId, BigDecimal total) {
        super(channel);
        this.orderId = Objects.requireNonNull(orderId);
        this.total = Objects.requireNonNull(total);
    }

    @Override
    protected String subject() {
        return "Order " + orderId + " confirmed";
    }

    @Override
    protected String body() {
        return "Your order " + orderId + " totalling $" + total + " has been confirmed.";
    }
}
