package com.jk.explore.bridge;

import java.math.BigDecimal;

/**
 * The trap, kept for contrast. Content and delivery are welded into one
 * class, so this exact same message-composition logic will have to be
 * retyped in {@link NaiveOrderConfirmationSms}.
 */
public final class NaiveOrderConfirmationEmail {

    private final String orderId;
    private final BigDecimal total;

    public NaiveOrderConfirmationEmail(String orderId, BigDecimal total) {
        this.orderId = orderId;
        this.total = total;
    }

    public void send(String recipient) {
        String subject = "Order " + orderId + " confirmed";
        String body = "Your order " + orderId + " totalling $" + total + " has been confirmed.";
        System.out.println("[EMAIL to " + recipient + "] " + subject + " -- " + body);
    }
}
