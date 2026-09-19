package com.jk.explore.valueobject.naive;

/** The way prices are usually first written: a double, and a currency that lives somewhere else. */
public final class NaivePricing {

    private NaivePricing() {
    }

    public static double total(double unitPrice, int quantity) {
        double total = 0;
        for (int i = 0; i < quantity; i++) {
            total += unitPrice;
        }
        return total;
    }

    /** Nothing stops this adding pounds to dollars. The currency is just a string beside the number. */
    public static double add(double first, String firstCurrency, double second, String secondCurrency) {
        return first + second;
    }

    /** Three ways to split a bill, done with arithmetic that looks right. */
    public static double[] splitThreeWays(double total) {
        double share = Math.round(total / 3 * 100) / 100.0;
        return new double[]{share, share, share};
    }
}
