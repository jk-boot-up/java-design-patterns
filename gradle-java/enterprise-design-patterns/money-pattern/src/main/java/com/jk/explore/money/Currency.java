package com.jk.explore.money;

/**
 * The currencies the shop sells in, each with how many digits follow the point.
 *
 * <p>Pounds and dollars have two (pence, cents); yen has none. Storing that
 * here means no other class has to know it.
 */
public enum Currency {
    GBP("£", 2),
    USD("$", 2),
    JPY("¥", 0);

    private final String symbol;
    private final int digits;

    Currency(String symbol, int digits) {
        this.symbol = symbol;
        this.digits = digits;
    }

    public String symbol() {
        return symbol;
    }

    /** Digits after the point: 2 for pounds, 0 for yen. */
    public int digits() {
        return digits;
    }
}
