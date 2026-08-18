package com.jk.explore.facade;

public class NotificationService {

    public void sendOrderConfirmation(String customerId, String orderId, String trackingId) {
        System.out.println("Notification: emailed customer " + customerId + " confirmation for order "
                + orderId + " (trackingId=" + trackingId + ")");
    }
}
