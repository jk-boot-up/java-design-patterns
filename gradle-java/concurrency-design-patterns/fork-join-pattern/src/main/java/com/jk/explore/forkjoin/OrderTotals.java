package com.jk.explore.forkjoin;

/** Order totals in pence, and the plain loop that adds them up. */
public final class OrderTotals {

    private OrderTotals() {
    }

    public static long[] generate(int n) {
        long[] totals = new long[n];
        for (int i = 0; i < n; i++) {
            totals[i] = 500 + (i * 37L) % 9000;
        }
        return totals;
    }

    public static long sequentialSum(long[] totals) {
        long sum = 0;
        for (long t : totals) {
            sum += t;
        }
        return sum;
    }
}
