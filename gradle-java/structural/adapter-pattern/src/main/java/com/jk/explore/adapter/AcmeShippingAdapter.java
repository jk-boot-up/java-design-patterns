package com.jk.explore.adapter;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Adapts the incompatible {@link AcmeShippingSdk} to the
 * {@link ShippingRateProvider} interface checkout code expects: converts
 * kilograms to pounds on the way in, and integer cents to dollars on the
 * way out.
 */
public final class AcmeShippingAdapter implements ShippingRateProvider {

    private static final BigDecimal KG_TO_LB = new BigDecimal("2.20462");
    private static final BigDecimal CENTS_PER_DOLLAR = new BigDecimal("100");

    private final AcmeShippingSdk sdk;

    public AcmeShippingAdapter(AcmeShippingSdk sdk) {
        this.sdk = sdk;
    }

    @Override
    public BigDecimal quoteRate(String destinationZip, double weightKg) {
        double weightLb = BigDecimal.valueOf(weightKg)
                .multiply(KG_TO_LB)
                .doubleValue();

        long cents = sdk.fetchCostInCents(destinationZip, weightLb);

        return BigDecimal.valueOf(cents)
                .divide(CENTS_PER_DOLLAR, 2, RoundingMode.HALF_UP);
    }
}
