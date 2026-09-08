package com.jk.explore.adapter;

import java.math.BigDecimal;

/**
 * The interface checkout code is written against: kilograms in, dollars out.
 */
public interface ShippingRateProvider {

    BigDecimal quoteRate(String destinationZip, double weightKg);
}
