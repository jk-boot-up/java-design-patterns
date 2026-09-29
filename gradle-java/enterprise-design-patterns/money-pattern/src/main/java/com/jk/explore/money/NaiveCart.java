package com.jk.explore.money;

import java.util.ArrayList;
import java.util.List;

/**
 * The obvious cart: every price is a double, and there is no currency at all.
 *
 * <p>It looks right and mostly is. The acts show where a double cannot hold
 * a price exactly, and where nothing stops pounds being added to dollars.
 */
public final class NaiveCart {

    private final List<double[]> lines = new ArrayList<>();   // {unit price, quantity}

    public void add(double unitPrice, int quantity) {
        lines.add(new double[] {unitPrice, quantity});
    }

    public double total() {
        double total = 0;
        for (double[] line : lines) {
            total += line[0] * line[1];
        }
        return total;
    }

    /** What a careless "to pence" conversion does: cut off the fraction. */
    public static long toPenceByTruncating(double pounds) {
        return (long) (pounds * 100);
    }
}
