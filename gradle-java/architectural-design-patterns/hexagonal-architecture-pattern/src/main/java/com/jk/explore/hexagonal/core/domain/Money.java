package com.jk.explore.hexagonal.core.domain;

/**
 * An amount of money, held in pence.
 *
 * <p>Pence as a {@code long}, never pounds as a {@code double}. A course that
 * taught architecture while quietly losing a penny to binary floating point
 * would be teaching the wrong lesson well. The conversion to pounds happens
 * once, at the edge, in {@link #toString()}.
 */
public record Money(long pence) {

    public static final Money ZERO = new Money(0);

    public static Money pounds(long whole, int andPence) {
        return new Money(whole * 100 + andPence);
    }

    public Money plus(Money other) {
        return new Money(pence + other.pence);
    }

    public Money times(int quantity) {
        return new Money(pence * quantity);
    }

    /** "£382.50" — the only place pence become pounds. */
    @Override
    public String toString() {
        return String.format("£%d.%02d", pence / 100, Math.abs(pence % 100));
    }
}
