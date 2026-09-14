package com.jk.explore.retry;

/** Proof that money moved once. */
public record Receipt(String chargeId, String orderId, Money amount) {

    @Override
    public String toString() {
        return chargeId + " " + amount;
    }
}
