package com.jk.explore.visitor;

import java.util.Objects;

/**
 * An amount of money, held as whole pence so that arithmetic is exact.
 *
 * <p>The constructor is private. The only way in is through one of the
 * static factory methods below, and each of them says in its name what its
 * argument means. {@code Money.pounds(5)} and {@code Money.pence(5)} are
 * both a single {@code long}, and a constructor could never have told them
 * apart.
 */
public final class Money implements Comparable<Money> {

    /** Reused for every zero amount. A static factory may cache; a constructor may not. */
    private static final Money ZERO = new Money(0);

    private final long pence;

    private Money(long pence) {
        this.pence = pence;
    }

    /** Zero pounds. Always the same instance. */
    public static Money zero() {
        return ZERO;
    }

    /** An amount given in whole pence — {@code Money.pence(250)} is £2.50. */
    public static Money pence(long pence) {
        return pence == 0 ? ZERO : new Money(pence);
    }

    /** An amount given in pounds — {@code Money.pounds(2.50)} is £2.50. */
    public static Money pounds(double pounds) {
        return pence(Math.round(pounds * 100));
    }

    /** Reads back what {@link #toString()} writes, so receipts can round-trip. */
    public static Money parse(String text) {
        String digits = text.replace("£", "").replace(",", "").trim();
        try {
            return pounds(Double.parseDouble(digits));
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("not an amount of money: \"" + text + "\"");
        }
    }

    public long asPence() {
        return pence;
    }

    public boolean isZero() {
        return pence == 0;
    }

    public Money plus(Money other) {
        return pence(pence + other.pence);
    }

    public Money minus(Money other) {
        return pence(pence - other.pence);
    }

    /** This amount, a whole number of times over — a line total. */
    public Money times(int count) {
        return pence(pence * count);
    }

    /** A share of this amount, rounded to the nearest penny. */
    public Money percent(int percent) {
        return pence(Math.round(pence * percent / 100.0));
    }

    /** The smaller of the two, so a discount never exceeds what is owed. */
    public Money cappedAt(Money ceiling) {
        return pence <= ceiling.pence ? this : ceiling;
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
        return pence < 0
                ? String.format("-£%,.2f", -pence / 100.0)
                : String.format("£%,.2f", pence / 100.0);
    }
}
