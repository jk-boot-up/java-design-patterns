package com.jk.explore.clean.usecases;

public class PaymentDeclinedException extends RuntimeException {

    public PaymentDeclinedException(String reason) {
        super(reason);
    }
}
