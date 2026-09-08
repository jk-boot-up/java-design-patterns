package com.jk.explore.adapter;

/**
 * A stand-in for a real third-party shipping SDK, exactly as it would arrive
 * in a jar we cannot edit: different method name, different parameter order,
 * weight in pounds instead of kilograms, and a price in integer cents
 * instead of dollars.
 */
public final class AcmeShippingSdk {

    /**
     * Looks up a shipping cost in whole cents.
     *
     * @param zip        destination ZIP code
     * @param poundsMass package weight, in pounds
     * @return price in integer cents
     */
    public long fetchCostInCents(String zip, double poundsMass) {
        // A deliberately simple stand-in formula: a $4.99 base rate plus
        // $1.10 per pound, rounded to the nearest cent.
        double dollars = 4.99 + poundsMass * 1.10;
        return Math.round(dollars * 100);
    }
}
