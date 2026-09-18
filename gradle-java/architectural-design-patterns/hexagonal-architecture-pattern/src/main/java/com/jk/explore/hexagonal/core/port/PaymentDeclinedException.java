package com.jk.explore.hexagonal.core.port;

/**
 * The payment gateway said no. Declared by the port, in the core's own
 * vocabulary, so the core can catch it without knowing which real network
 * — or fake — is behind {@link PaymentGateway}.
 */
public class PaymentDeclinedException extends RuntimeException {

    public PaymentDeclinedException(String reason) {
        super(reason);
    }
}
