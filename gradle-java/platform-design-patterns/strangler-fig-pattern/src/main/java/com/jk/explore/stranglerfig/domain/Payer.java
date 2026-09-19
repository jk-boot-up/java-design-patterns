package com.jk.explore.stranglerfig.domain;

public interface Payer {
    /** Returns a charge id, or null if the payment failed. */
    String charge(long totalPence);
}
