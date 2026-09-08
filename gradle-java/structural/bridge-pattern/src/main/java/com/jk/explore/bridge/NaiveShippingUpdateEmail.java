package com.jk.explore.bridge;

/** The trap, kept for contrast. A second notification type, a second pair of classes. */
public final class NaiveShippingUpdateEmail {

    private final String orderId;
    private final String status;

    public NaiveShippingUpdateEmail(String orderId, String status) {
        this.orderId = orderId;
        this.status = status;
    }

    public void send(String recipient) {
        String subject = "Shipping update for order " + orderId;
        String body = "Order " + orderId + " is now: " + status;
        System.out.println("[EMAIL to " + recipient + "] " + subject + " -- " + body);
    }
}
