package com.jk.explore.valueobject.domain;

import java.util.ArrayList;
import java.util.List;

/**
 * An amount of money: whole pence and a currency, together, forever.
 *
 * <p>A value object. It has no identity, only value, so two of them with the same pence and currency are
 * the same money and {@code equals} says so. It never changes: every operation returns a new one, so it can
 * be shared between orders with no fear that one order alters another's price. It cannot be built in a
 * state that makes no sense, and it refuses to be combined with money in another currency.
 */
public record Money(long pence, String currency) {

    public Money {
        if (currency == null || currency.length() != 3) {
            throw new IllegalArgumentException("a currency is three letters, such as GBP");
        }
    }

    public static Money gbp(long pence) {
        return new Money(pence, "GBP");
    }

    public static Money usd(long cents) {
        return new Money(cents, "USD");
    }

    public Money plus(Money other) {
        sameCurrency(other);
        return new Money(pence + other.pence, currency);
    }

    public Money minus(Money other) {
        sameCurrency(other);
        return new Money(pence - other.pence, currency);
    }

    public Money times(int quantity) {
        return new Money(pence * quantity, currency);
    }

    /**
     * Splits this amount into {@code parts} shares that add back to exactly this amount. Whole pence cannot
     * always be split evenly, so the first shares each take one extra penny until the remainder is used up.
     */
    public List<Money> allocate(int parts) {
        if (parts < 1) {
            throw new IllegalArgumentException("split into at least one part");
        }
        long base = Math.floorDiv(pence, parts);
        long remainder = Math.floorMod(pence, parts);
        List<Money> shares = new ArrayList<>();
        for (int i = 0; i < parts; i++) {
            shares.add(new Money(base + (i < remainder ? 1 : 0), currency));
        }
        return shares;
    }

    private void sameCurrency(Money other) {
        if (!currency.equals(other.currency)) {
            throw new CurrencyMismatch(currency, other.currency);
        }
    }

    @Override
    public String toString() {
        return String.format("%s %s%d.%02d", currency, pence < 0 ? "-" : "", Math.abs(pence) / 100, Math.abs(pence) % 100);
    }
}
