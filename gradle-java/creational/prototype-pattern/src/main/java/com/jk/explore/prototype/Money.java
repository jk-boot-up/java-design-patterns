package com.jk.explore.prototype;

import java.util.Objects;

/**
 * An amount of money, held as whole pence so that arithmetic is exact.
 *
 * <p>Not the point of this project — {@link ProductListing} is — but built
 * the way the static factory method project recommends: private
 * constructor, named static factories. Patterns compose; the values a
 * prototype is filled with can still be simple, well-made ones.
 */
public final class Money implements Comparable<Money> {

    private static final Money ZERO = new Money(0);

    private final long pence;

    private Money(long pence) {
        this.pence = pence;
    }

    public static Money zero() {
        return ZERO;
    }

    public static Money pence(long pence) {
        return pence == 0 ? ZERO : new Money(pence);
    }

    public static Money pounds(double pounds) {
        return pence(Math.round(pounds * 100));
    }

    public long asPence() {
        return pence;
    }

    @Override
    public int compareTo(Money other) {
        return Long.compare(pence, other.pence);
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof Money money && money.pence == pence;
    }

    @Override
    public int hashCode() {
        return Objects.hash(pence);
    }

    @Override
    public String toString() {
        return String.format("£%,.2f", pence / 100.0);
    }
}
