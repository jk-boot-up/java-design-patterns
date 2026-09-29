package com.jk.explore.railwayvavr;

/**
 * The payment company's client library: it reports a declined card by throwing, as much Java code does.
 */
public final class LegacyPayments {

    public static String charge(String card, double amount) {
        if (card.endsWith("0002")) {
            throw new IllegalStateException("card declined");
        }
        return "ORD-1";
    }

    private LegacyPayments() {
    }
}
