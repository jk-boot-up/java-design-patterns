package com.jk.explore.facade;

import java.util.UUID;

public class ShippingService {

    public String scheduleShipment(String orderId, String address) {
        String trackingId = "TRK-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
        System.out.println("Shipping: scheduled shipment for order " + orderId + " to " + address
                + " (trackingId=" + trackingId + ")");
        return trackingId;
    }
}
