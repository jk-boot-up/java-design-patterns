package com.jk.explore.apigateway;

import java.util.Map;

/**
 * The Pricing service: what something costs today.
 *
 * Separate from Catalog because prices change on a different schedule from
 * product descriptions, and by different people.
 */
public final class PricingService {

    private final Map<String, Money> prices = Map.of(
            "SKU-1234", Money.pence(44999),
            "SKU-2001", Money.pence(1850),
            "SKU-2002", Money.pence(1299));

    public Money price(String sku) {
        Money price = prices.get(sku);
        if (price == null) {
            throw new IllegalArgumentException("no price for " + sku);
        }
        return price;
    }
}
