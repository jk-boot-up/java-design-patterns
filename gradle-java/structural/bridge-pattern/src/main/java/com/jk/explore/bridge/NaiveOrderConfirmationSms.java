package com.jk.explore.bridge;

import java.math.BigDecimal;

/**
 * The trap, kept for contrast. The truncation logic here is copied from
 * {@link SmsChannel}, and it will be copied again into
 * {@link NaiveShippingUpdateSms} -- every naive SMS class re-derives the
 * exact same "how does SMS work" answer.
 */
public final class NaiveOrderConfirmationSms {

    private final String orderId;
    private final BigDecimal total;

    public NaiveOrderConfirmationSms(String orderId, BigDecimal total) {
        this.orderId = orderId;
        this.total = total;
    }

    public void send(String recipient) {
        String subject = "Order " + orderId + " confirmed";
        String body = "Your order " + orderId + " totalling $" + total + " has been confirmed.";
        String text = subject + ": " + body;
        if (text.length() > SmsChannel.MAX_LENGTH) {
            text = text.substring(0, SmsChannel.MAX_LENGTH - 1) + "…";
        }
        System.out.println("[SMS to " + recipient + "] " + text);
    }
}
