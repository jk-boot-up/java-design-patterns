package com.jk.explore.hexagonalspring.core.port;

/** Driven port: taking money. Throws {@code PaymentRefused} when the card is declined. */
public interface Payments {
    void charge(long pence);
}
