package com.jk.explore.cleanspring.usecases;

public class PaymentDeclinedException extends RuntimeException {

    public PaymentDeclinedException(String reason) {
        super(reason);
    }
}
