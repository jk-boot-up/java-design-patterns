package com.jk.explore.templatemethod;

/**
 * Thrown when a step cannot complete — no address on a shipped order, not
 * enough stock, a seller that will not confirm.
 *
 * <p>It stops the template method where it stands, which is the point: the
 * sequence is a sequence, and a later step must never run on the assumption
 * that an earlier one succeeded.
 */
public class FulfilmentException extends RuntimeException {

    public FulfilmentException(String message) {
        super(message);
    }
}
