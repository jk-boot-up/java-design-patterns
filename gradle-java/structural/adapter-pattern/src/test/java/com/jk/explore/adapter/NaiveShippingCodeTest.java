package com.jk.explore.adapter;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Confirms the naive, SDK-coupled classes compute the exact same rate as
 * the adapter -- the naive approach is not wrong, it is just duplicated and
 * coupled directly to a third-party shape.
 */
class NaiveShippingCodeTest {

    @Test
    void naiveCheckoutServiceMatchesTheAdapter() {
        BigDecimal naive = new NaiveCheckoutService().shippingCost("94107", 3.5);
        BigDecimal adapted = new AcmeShippingAdapter(new AcmeShippingSdk()).quoteRate("94107", 3.5);
        assertEquals(adapted, naive);
    }

    @Test
    void naiveShippingEstimatorMatchesTheAdapter() {
        BigDecimal naive = new NaiveShippingEstimator().estimate("94107", 3.5);
        BigDecimal adapted = new AcmeShippingAdapter(new AcmeShippingSdk()).quoteRate("94107", 3.5);
        assertEquals(adapted, naive);
    }
}
