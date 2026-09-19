package com.jk.explore.activerecord;

/** The same delivery rule with no record behind it: it takes the two numbers it needs. */
public final class PureDiscount {

    private PureDiscount() {
    }

    public static boolean qualifiesForFreeDelivery(long totalPence, long thresholdPence) {
        return totalPence >= thresholdPence;
    }
}
