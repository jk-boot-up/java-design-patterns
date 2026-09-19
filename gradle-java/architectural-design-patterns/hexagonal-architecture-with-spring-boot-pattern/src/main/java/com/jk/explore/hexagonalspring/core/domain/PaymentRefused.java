package com.jk.explore.hexagonalspring.core.domain;

public class PaymentRefused extends RuntimeException {
    public PaymentRefused() {
        super("the card was declined");
    }
}
