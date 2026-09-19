package com.jk.explore.gateway;

/** What the shop wants to know about a payment, in the shop's words. */
public record PaymentResult(PaymentStatus status, String receipt) {

    public boolean approved() {
        return status == PaymentStatus.APPROVED;
    }
}
