package com.jk.explore.sidecar;

/**
 * The payment did not go through.
 *
 * <p>The {@link Reason} matters more than the message. {@code WOBBLE} is the gateway
 * having a bad minute and is worth retrying; {@code RATE_LIMITED} is the gateway saying
 * "you personally are asking too often" and retrying it makes the situation worse, not
 * better. Code that treats those two the same is how a small outage becomes a large one.
 */
public class PaymentFailed extends RuntimeException {

    public enum Reason {
        /** The gateway is having a bad minute. Trying again shortly usually works. */
        WOBBLE,
        /** The gateway has cut this merchant account off for asking too often. */
        RATE_LIMITED,
        /** Nothing answered at the address at all. */
        NOTHING_LISTENING
    }

    private final Reason reason;

    public PaymentFailed(Reason reason, String message) {
        super(message);
        this.reason = reason;
    }

    public Reason reason() {
        return reason;
    }
}
