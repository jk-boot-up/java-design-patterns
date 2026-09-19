package com.jk.explore.readwritelock.naive;

import com.jk.explore.readwritelock.domain.Price;

import java.math.BigDecimal;

/**
 * <strong>No synchronization at all.</strong> A price update changes two
 * fields, one after the other — there is no way to change both at once
 * without something serializing the two writes against a concurrent read.
 * A reader unlucky enough to read between the two writes sees a price that
 * was never true at any moment: the new amount, in the old currency, or
 * the other way round.
 *
 * <p>{@code midWrite} is a seam for forcing that exact interleaving on
 * purpose, in a test, rather than hoping a race shows up: a
 * {@link com.jk.explore.readwritelock.harness.Gate} passed here parks the
 * writer between the two field assignments so a reader can be proven to
 * run in the gap.
 */
public final class UnsynchronizedCatalogue {

    private BigDecimal amount;
    private String currency;
    private final Runnable midWrite;

    public UnsynchronizedCatalogue(Price initial, Runnable midWrite) {
        this.amount = initial.amount();
        this.currency = initial.currency();
        this.midWrite = midWrite;
    }

    public UnsynchronizedCatalogue(Price initial) {
        this(initial, () -> { });
    }

    public Price read() {
        return new Price(amount, currency);
    }

    public void write(Price price) {
        this.amount = price.amount();
        midWrite.run();
        this.currency = price.currency();
    }
}
