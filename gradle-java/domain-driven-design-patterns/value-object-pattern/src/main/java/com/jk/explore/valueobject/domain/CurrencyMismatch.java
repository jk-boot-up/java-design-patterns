package com.jk.explore.valueobject.domain;

/** Two amounts in different currencies were combined. The type refuses, instead of guessing a rate. */
public class CurrencyMismatch extends RuntimeException {
    public CurrencyMismatch(String left, String right) {
        super("cannot combine " + left + " with " + right);
    }
}
