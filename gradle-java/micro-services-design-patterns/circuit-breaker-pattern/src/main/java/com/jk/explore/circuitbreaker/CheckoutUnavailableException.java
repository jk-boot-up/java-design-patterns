package com.jk.explore.circuitbreaker;

/**
 * The shop cannot take payment right now, and says so.
 *
 * This is what an honest fallback looks like when there is nothing sensible to fall
 * back to: a clear message, delivered immediately, that leaves the shopper's basket
 * intact and their card untouched.
 */
public class CheckoutUnavailableException extends RuntimeException {

    public CheckoutUnavailableException(String message) {
        super(message);
    }
}
