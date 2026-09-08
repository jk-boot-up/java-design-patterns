package com.jk.explore.adapter;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * A second, unrelated place in the codebase that also needs a shipping
 * quote — and, with no shared abstraction, has to duplicate the exact same
 * pounds/cents conversion that {@link NaiveCheckoutService} already wrote.
 */
public final class NaiveShippingEstimator {

    private final AcmeShippingSdk sdk = new AcmeShippingSdk();

    public BigDecimal estimate(String destinationZip, double weightKg) {
        double weightLb = weightKg * 2.20462;
        long cents = sdk.fetchCostInCents(destinationZip, weightLb);
        return BigDecimal.valueOf(cents).divide(new BigDecimal("100"), 2, RoundingMode.HALF_UP);
    }
}
