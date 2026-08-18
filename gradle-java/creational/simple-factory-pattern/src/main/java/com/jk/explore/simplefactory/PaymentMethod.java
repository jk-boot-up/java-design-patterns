package com.jk.explore.simplefactory;

public sealed interface PaymentMethod
        permits CreditCardPayment, UpiPayment, PayPalPayment, NetBankingPayment {

    String displayName();

    PaymentReceipt pay(PaymentRequest request);
}
