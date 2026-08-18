package com.jk.explore.facade;

import java.util.UUID;

public class PaymentService {

    public String charge(String customerId, double amount) {
        String paymentId = "PMT-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
        System.out.println("Payment: charged $" + amount + " to customer " + customerId
                + " (paymentId=" + paymentId + ")");
        return paymentId;
    }
}
