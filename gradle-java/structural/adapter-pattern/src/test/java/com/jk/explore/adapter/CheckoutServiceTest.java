package com.jk.explore.adapter;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

class CheckoutServiceTest {

    @Test
    void addsTheAdaptedProvidersQuoteToTheSubtotal() {
        CheckoutService checkout = new CheckoutService(new AcmeShippingAdapter(new AcmeShippingSdk()));
        assertEquals(new BigDecimal("63.46"), checkout.totalWithShipping(new BigDecimal("49.98"), "94107", 3.5));
    }

    @Test
    void worksIdenticallyWithANativeProvider() {
        CheckoutService checkout = new CheckoutService(new FlatRateShippingProvider());
        assertEquals(new BigDecimal("57.48"), checkout.totalWithShipping(new BigDecimal("49.98"), "94107", 3.5));
    }
}
