package com.jk.explore.servicelayer.domain;

public class OrderRejectedException extends RuntimeException {

    public OrderRejectedException(String reason) {
        super(reason);
    }
}
