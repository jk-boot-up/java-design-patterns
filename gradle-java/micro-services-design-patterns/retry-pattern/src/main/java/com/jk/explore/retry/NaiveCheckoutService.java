package com.jk.explore.retry;

/**
 * Checkout with the retry loop everybody writes first.
 *
 * Read it and it looks reasonable. It is three lines, it has no dependencies, and
 * it does turn a flaky gateway into a successful checkout most of the time. It has
 * three faults and not one of them shows up as a failing test:
 *
 * <ol>
 *   <li>A fresh idempotency key on every attempt, because the request is built
 *       inside the loop. The gateway therefore cannot tell the second attempt from
 *       a genuinely new order, and charges the customer again.</li>
 *   <li>No delay, so it retries as fast as the network allows. When the gateway is
 *       slow because it is overloaded, this is the overload.</li>
 *   <li>No idea which failures are worth retrying, so a declined card is asked
 *       three times and answered "no" three times.</li>
 * </ol>
 */
public final class NaiveCheckoutService {

    private static final int ATTEMPTS = 3;

    private final PaymentGateway payments;
    private final CallLog log;

    public NaiveCheckoutService(PaymentGateway payments, CallLog log) {
        this.payments = payments;
        this.log = log;
    }

    /** Tries three times, immediately, with a new key each time. */
    public Receipt pay(String orderId, Money amount) {
        RuntimeException last = null;
        for (int attempt = 1; attempt <= ATTEMPTS; attempt++) {
            try {
                // A new key per attempt. This is the double charge, right here.
                PaymentRequest request = new PaymentRequest(orderId, amount,
                        "key-" + orderId + "-attempt-" + attempt);
                return payments.charge(request);
            } catch (RuntimeException e) {
                last = e;
                log.note("NaiveCheckout", "RETRYING", "attempt " + attempt
                        + " failed, going again immediately");
            }
        }
        throw last;
    }
}
