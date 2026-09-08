package com.jk.explore.bridge;

/**
 * The trap, kept for contrast. The same truncation logic as
 * {@link NaiveOrderConfirmationSms}, copied a second time.
 */
public final class NaiveShippingUpdateSms {

    private final String orderId;
    private final String status;

    public NaiveShippingUpdateSms(String orderId, String status) {
        this.orderId = orderId;
        this.status = status;
    }

    public void send(String recipient) {
        String subject = "Shipping update for order " + orderId;
        String body = "Order " + orderId + " is now: " + status;
        String text = subject + ": " + body;
        if (text.length() > SmsChannel.MAX_LENGTH) {
            text = text.substring(0, SmsChannel.MAX_LENGTH - 1) + "…";
        }
        System.out.println("[SMS to " + recipient + "] " + text);
    }
}
