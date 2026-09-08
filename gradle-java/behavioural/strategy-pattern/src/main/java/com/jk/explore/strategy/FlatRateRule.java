package com.jk.explore.strategy;

import java.util.Objects;

/**
 * The same price for every delivery, whatever it weighs and however far it
 * goes.
 *
 * <p>The simplest rule in the shop, and the one that shows what the interface
 * really asks for: it ignores every field on the {@link Shipment} and still
 * satisfies the contract. A strategy is not obliged to use its input, only to
 * accept it.
 */
public final class FlatRateRule implements ShippingCostRule {

    private final Money rate;

    public FlatRateRule(Money rate) {
        this.rate = Objects.requireNonNull(rate, "rate");
    }

    @Override
    public String name() {
        return "Flat rate";
    }

    @Override
    public Money costFor(Shipment shipment) {
        return rate;
    }
}
