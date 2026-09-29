package com.jk.explore.money;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Objects;

/**
 * An amount of money: a whole number of the smallest unit, plus its currency.
 *
 * <p>£19.99 is stored as 1999 pence and GBP. Whole numbers add, subtract and
 * multiply exactly, so no penny is ever lost to rounding, and the currency
 * travels with the amount, so pounds are never added to dollars by mistake.
 * A Money never changes: every operation returns a new one.
 */
public final class Money implements Comparable<Money> {

    private final long minor;
    private final Currency currency;

    private Money(long minor, Currency currency) {
        this.minor = minor;
        this.currency = Objects.requireNonNull(currency);
    }

    /** Money from its smallest unit: ofMinor(1999, GBP) is £19.99. */
    public static Money ofMinor(long minor, Currency currency) {
        return new Money(minor, currency);
    }

    /** Money from written text: of("19.99", GBP). Refuses more digits than the currency has. */
    public static Money of(String amount, Currency currency) {
        BigDecimal value = new BigDecimal(amount);
        if (value.scale() > currency.digits()) {
            throw new IllegalArgumentException(amount + " has more digits than " + currency + " allows");
        }
        return new Money(value.movePointRight(currency.digits()).longValueExact(), currency);
    }

    public static Money zero(Currency currency) {
        return new Money(0, currency);
    }

    public long minor() {
        return minor;
    }

    public Currency currency() {
        return currency;
    }

    public Money plus(Money other) {
        requireSameCurrency(other);
        return new Money(Math.addExact(minor, other.minor), currency);
    }

    public Money minus(Money other) {
        requireSameCurrency(other);
        return new Money(Math.subtractExact(minor, other.minor), currency);
    }

    /** Multiply by a whole number, for example a quantity: exact. */
    public Money times(int quantity) {
        return new Money(Math.multiplyExact(minor, quantity), currency);
    }

    /**
     * Multiply by a rate such as 0.20 for VAT. The result can fall between two
     * pennies, so the caller must say how to round: nothing is rounded silently.
     */
    public Money times(String rate, RoundingMode rounding) {
        BigDecimal exact = BigDecimal.valueOf(minor).multiply(new BigDecimal(rate));
        return new Money(exact.setScale(0, rounding).longValueExact(), currency);
    }

    /**
     * Split into shares by ratio, such as {1, 1, 1} for three equal parts or {70, 30}.
     *
     * <p>Each share is rounded down, and the pennies left over go one at a time
     * to the first shares. The shares always add back to exactly this amount.
     */
    public Money[] allocate(long... ratios) {
        long total = 0;
        for (long r : ratios) {
            total += r;
        }
        Money[] shares = new Money[ratios.length];
        long given = 0;
        for (int i = 0; i < ratios.length; i++) {
            long share = minor * ratios[i] / total;
            shares[i] = new Money(share, currency);
            given += share;
        }
        for (int i = 0; given < minor; i++, given++) {
            shares[i] = new Money(shares[i].minor + 1, currency);
        }
        return shares;
    }

    public boolean isGreaterThan(Money other) {
        return compareTo(other) > 0;
    }

    @Override
    public int compareTo(Money other) {
        requireSameCurrency(other);
        return Long.compare(minor, other.minor);
    }

    private void requireSameCurrency(Money other) {
        if (other.currency != currency) {
            throw new IllegalArgumentException("cannot combine " + currency + " with " + other.currency);
        }
    }

    @Override
    public boolean equals(Object o) {
        return o instanceof Money m && m.minor == minor && m.currency == currency;
    }

    @Override
    public int hashCode() {
        return Objects.hash(minor, currency);
    }

    /** £19.99, $5.00, ¥1500. */
    @Override
    public String toString() {
        BigDecimal value = BigDecimal.valueOf(minor, currency.digits());
        return currency.symbol() + value.toPlainString();
    }
}
