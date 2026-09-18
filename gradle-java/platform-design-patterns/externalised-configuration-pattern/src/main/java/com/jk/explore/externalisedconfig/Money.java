package com.jk.explore.externalisedconfig;

import java.util.Optional;
import java.util.regex.Pattern;

/**
 * An amount of money, held as a whole number of pence.
 *
 * <p>Pence rather than pounds, and a {@code long} rather than a {@code double},
 * because money in a shop is counted, not measured. There is no such thing as
 * half a penny on an invoice, and the moment you store £4.99 as a floating
 * point number you have signed up for totals that are a penny out and nobody
 * can say why.
 *
 * <p>{@link #parse(String)} is the interesting method in this project. Every
 * value that arrives from outside the program arrives as text — a line in a
 * file, a field on a web form, an environment variable — and text is where the
 * trouble starts. It returns an {@link Optional} rather than throwing, because
 * "this is not a number" is an ordinary thing for outside input to be, and the
 * caller is better placed than this class to decide what to do about it.
 *
 * <p>Note what {@code parse} does <em>not</em> reject: a negative amount.
 * {@code "-1"} is a perfectly well-formed number, so it parses happily into
 * minus one pound. Whether minus one pound is a sensible free-delivery
 * threshold is a different question, and asking it is somebody else's job —
 * see {@link MoneySetting}.
 */
public record Money(long pence) implements Comparable<Money> {

    private static final Pattern WELL_FORMED = Pattern.compile("-?\\d+(\\.\\d{1,2})?");

    /** An amount given in whole pounds, so {@code pounds(50)} is £50.00. */
    public static Money pounds(long pounds) {
        return new Money(pounds * 100);
    }

    /** An amount given in pence, so {@code pence(499)} is £4.99. */
    public static Money pence(long pence) {
        return new Money(pence);
    }

    /** Nothing at all. What free delivery costs the customer. */
    public static Money zero() {
        return new Money(0);
    }

    /**
     * Reads an amount out of text, or reports that the text was not an amount.
     *
     * <p>Accepts {@code "50"}, {@code "35.00"} and {@code "4.99"}, and also
     * {@code "-1"}, which is well formed and negative. Refuses {@code "fifty"},
     * {@code ""} and {@code "50 pounds"}, because none of those is a number
     * however sympathetically you squint at it.
     */
    public static Optional<Money> parse(String text) {
        if (text == null) {
            return Optional.empty();
        }
        String trimmed = text.trim();
        if (!WELL_FORMED.matcher(trimmed).matches()) {
            return Optional.empty();
        }
        boolean negative = trimmed.startsWith("-");
        String digits = negative ? trimmed.substring(1) : trimmed;
        int dot = digits.indexOf('.');
        long pounds = Long.parseLong(dot < 0 ? digits : digits.substring(0, dot));
        long pennies = 0;
        if (dot >= 0) {
            String fraction = digits.substring(dot + 1);
            pennies = Long.parseLong(fraction.length() == 1 ? fraction + "0" : fraction);
        }
        long total = pounds * 100 + pennies;
        return Optional.of(new Money(negative ? -total : total));
    }

    /** True when this amount is the same as, or larger than, the other one. */
    public boolean isAtLeast(Money other) {
        return this.pence >= other.pence;
    }

    /** True when this amount is below zero. A threshold never should be. */
    public boolean isNegative() {
        return pence < 0;
    }

    @Override
    public int compareTo(Money other) {
        return Long.compare(this.pence, other.pence);
    }

    /** Written the way a customer would see it, so {@code £50.00}. */
    @Override
    public String toString() {
        long absolute = Math.abs(pence);
        return (pence < 0 ? "-£" : "£") + (absolute / 100) + "." + String.format("%02d", absolute % 100);
    }
}
