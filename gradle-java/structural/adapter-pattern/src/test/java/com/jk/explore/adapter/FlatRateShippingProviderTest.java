package com.jk.explore.adapter;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

class FlatRateShippingProviderTest {

    @Test
    void alwaysQuotesTheFlatRate() {
        ShippingRateProvider provider = new FlatRateShippingProvider();
        assertEquals(new BigDecimal("7.50"), provider.quoteRate("94107", 0.5));
        assertEquals(new BigDecimal("7.50"), provider.quoteRate("10001", 20.0));
    }
}
