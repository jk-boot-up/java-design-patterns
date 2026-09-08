package com.jk.explore.adapter;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * The trap: checkout code that talks to {@link AcmeShippingSdk} directly.
 * It has to know the SDK's units (pounds, cents) and redo the conversion
 * itself, right here in business logic that should only care about
 * kilograms and dollars.
 */
public final class NaiveCheckoutService {

    private final AcmeShippingSdk sdk = new AcmeShippingSdk();

    public BigDecimal shippingCost(String destinationZip, double weightKg) {
        double weightLb = weightKg * 2.20462;
        long cents = sdk.fetchCostInCents(destinationZip, weightLb);
        return BigDecimal.valueOf(cents).divide(new BigDecimal("100"), 2, RoundingMode.HALF_UP);
    }
}
