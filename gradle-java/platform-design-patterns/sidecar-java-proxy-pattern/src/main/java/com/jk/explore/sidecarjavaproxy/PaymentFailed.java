package com.jk.explore.sidecarjavaproxy;

/**
 * The payment did not go through.
 *
 * <p>The {@link Reason} matters more than the message. {@code WOBBLE} is the provider
 * having a bad minute and is worth trying again; {@code RATE_LIMITED} is the provider
 * saying "you personally are asking too often", and trying that again makes things
 * worse. Both proxies in this project have to tell those two apart, and both of them do,
 * which is one of the few things they agree on completely.
 */
public class PaymentFailed extends RuntimeException {

    public enum Reason {
        /** The provider is having a bad moment. Asking again shortly usually works. */
        WOBBLE,
        /** The provider has cut this merchant account off for asking too often. */
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
