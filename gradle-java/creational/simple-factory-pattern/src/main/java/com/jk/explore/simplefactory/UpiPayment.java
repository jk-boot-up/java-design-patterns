package com.jk.explore.simplefactory;

import java.util.UUID;

public final class UpiPayment implements PaymentMethod {

    @Override
    public String displayName() {
        return "UPI";
    }

    @Override
    public PaymentReceipt pay(PaymentRequest request) {
        System.out.println("UPI: sending a collect request to " + request.customerId());
        System.out.println("UPI: customer approved " + request.amount() + " in the payments app");
        return new PaymentReceipt(newTransactionId(), displayName(), request.amount());
    }

    private static String newTransactionId() {
        return "UPI-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    }
}
