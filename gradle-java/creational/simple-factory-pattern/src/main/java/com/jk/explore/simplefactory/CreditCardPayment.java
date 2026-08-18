package com.jk.explore.simplefactory;

import java.util.UUID;

public final class CreditCardPayment implements PaymentMethod {

    @Override
    public String displayName() {
        return "Credit Card";
    }

    @Override
    public PaymentReceipt pay(PaymentRequest request) {
        System.out.println("Credit Card: authorising " + request.amount() + " for order " + request.orderId());
        System.out.println("Credit Card: capturing the authorised amount");
        return new PaymentReceipt(newTransactionId(), displayName(), request.amount());
    }

    private static String newTransactionId() {
        return "CC-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    }
}
