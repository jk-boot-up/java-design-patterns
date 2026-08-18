package com.jk.explore.simplefactory;

import java.util.UUID;

public final class PayPalPayment implements PaymentMethod {

    @Override
    public String displayName() {
        return "PayPal";
    }

    @Override
    public PaymentReceipt pay(PaymentRequest request) {
        System.out.println("PayPal: redirecting " + request.customerId() + " to the PayPal checkout");
        System.out.println("PayPal: payment of " + request.amount() + " completed");
        return new PaymentReceipt(newTransactionId(), displayName(), request.amount());
    }

    private static String newTransactionId() {
        return "PP-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    }
}
