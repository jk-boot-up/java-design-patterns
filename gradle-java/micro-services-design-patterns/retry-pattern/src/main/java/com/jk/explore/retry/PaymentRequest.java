package com.jk.explore.retry;

/**
 * One attempt to take money for one order.
 *
 * The {@code idempotencyKey} is the field that matters, and it is worth being
 * precise about what it means: it is a promise from the caller that says "if you
 * have already seen this key, you have already done this job — do not do it again,
 * just tell me what happened last time".
 *
 * <p>Without it, retrying a payment is not a retry. It is a second payment.
 */
public record PaymentRequest(String orderId, Money amount, String idempotencyKey) {

    /**
     * The key a careful caller uses: one key per order, reused by every attempt.
     *
     * Note what it is derived from — the order, and nothing else. Not the attempt
     * number, not the clock, not a random value. If any of those crept in, each
     * attempt would carry a different key and the gateway would have no way to
     * recognise the repeat.
     */
    public static PaymentRequest forOrder(String orderId, Money amount) {
        return new PaymentRequest(orderId, amount, "key-" + orderId);
    }
}
