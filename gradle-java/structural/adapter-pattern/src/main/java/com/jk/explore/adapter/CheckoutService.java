package com.jk.explore.adapter;

import java.math.BigDecimal;
import java.util.Objects;

/**
 * Checkout logic written entirely against {@link ShippingRateProvider}.
 * It never mentions Acme, pounds, or cents -- and works identically whether
 * the provider underneath is an adapted third-party SDK or a
 * natively-written one.
 */
public final class CheckoutService {

    private final ShippingRateProvider shippingRateProvider;

    public CheckoutService(ShippingRateProvider shippingRateProvider) {
        this.shippingRateProvider = Objects.requireNonNull(shippingRateProvider);
    }

    public BigDecimal totalWithShipping(BigDecimal itemsSubtotal, String destinationZip, double weightKg) {
        BigDecimal shipping = shippingRateProvider.quoteRate(destinationZip, weightKg);
        return itemsSubtotal.add(shipping);
    }
}
