package com.jk.explore.entity;

/**
 * A customer's identity: given once, when the account is opened, and never changed.
 */
public record CustomerId(String value) {

    @Override
    public String toString() {
        return value;
    }
}
