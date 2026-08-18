package com.jk.explore.simplefactory;

import java.util.UUID;

public final class NetBankingPayment implements PaymentMethod {

    @Override
    public String displayName() {
        return "Net Banking";
    }

    @Override
    public PaymentReceipt pay(PaymentRequest request) {
        System.out.println("Net Banking: opening the bank's login page for " + request.customerId());
        System.out.println("Net Banking: bank confirmed a transfer of " + request.amount());
        return new PaymentReceipt(newTransactionId(), displayName(), request.amount());
    }

    private static String newTransactionId() {
        return "NB-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    }
}
