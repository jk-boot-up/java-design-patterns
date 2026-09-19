package com.jk.explore.layeredspring.infrastructure;

public class PaymentDeclined extends RuntimeException {
    public PaymentDeclined() {
        super("the card was declined");
    }
}
