package com.jk.explore.sidecar;

/**
 * One request to take money, as the payment provider sees it.
 *
 * <p>The {@code idempotencyKey} is not decoration. Anything that retries a payment
 * needs the provider to recognise a repeat and charge once, and the whole of this
 * project is about retrying payments. It is here so that nobody reading the retry code
 * later has to wonder whether four attempts meant four charges.
 */
public record Payment(String orderRef, int amountPence, String idempotencyKey) {

    public static Payment of(String orderRef, int amountPence) {
        return new Payment(orderRef, amountPence, "idem-" + orderRef);
    }
}
