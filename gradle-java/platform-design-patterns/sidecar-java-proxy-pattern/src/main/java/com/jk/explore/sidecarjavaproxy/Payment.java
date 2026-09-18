package com.jk.explore.sidecarjavaproxy;

/**
 * One request to take money, as the payment provider sees it.
 *
 * <p>The {@code idempotencyKey} is what makes retrying a payment safe at all: the
 * provider recognises a repeat and charges once. Both proxies in this project retry, so
 * both of them depend on that promise, and neither of them would be allowed to exist
 * without it.
 */
public record Payment(String orderRef, int amountPence, String idempotencyKey) {

    public static Payment of(String orderRef, int amountPence) {
        return new Payment(orderRef, amountPence, "idem-" + orderRef);
    }
}
