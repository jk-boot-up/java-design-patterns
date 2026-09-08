package com.jk.explore.adapter;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

class AcmeShippingAdapterTest {

    private final ShippingRateProvider adapter = new AcmeShippingAdapter(new AcmeShippingSdk());

    @Test
    void convertsKilogramsToPoundsAndCentsToDollars() {
        assertEquals(new BigDecimal("13.48"), adapter.quoteRate("94107", 3.5));
    }

    @Test
    void zeroWeightStillChargesTheBaseRate() {
        assertEquals(new BigDecimal("4.99"), adapter.quoteRate("94107", 0.0));
    }

    @Test
    void roundsToTheNearestCent() {
        // 1.0 kg -> 2.20462 lb -> 4.99 + 2.20462*1.10 = 7.415082 dollars -> rounds to 7.42
        assertEquals(new BigDecimal("7.42"), adapter.quoteRate("94107", 1.0));
    }
}
