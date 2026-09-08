package com.jk.explore.adapter;

import java.math.BigDecimal;

/**
 * A shipping provider written natively against {@link ShippingRateProvider}
 * -- no adapter needed, because it was designed to speak the target
 * interface from the start. Included to show that checkout code cannot
 * tell this apart from {@link AcmeShippingAdapter} at the call site.
 */
public final class FlatRateShippingProvider implements ShippingRateProvider {

    private static final BigDecimal FLAT_RATE = new BigDecimal("7.50");

    @Override
    public BigDecimal quoteRate(String destinationZip, double weightKg) {
        return FLAT_RATE;
    }
}
