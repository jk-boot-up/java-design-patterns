package com.jk.explore.strategy;

import java.util.Objects;

/**
 * Quotes an order, delivery included — the Strategy client.
 *
 * <p>Search this class for "flat", "weight" or "distance" and you find
 * nothing. It holds a {@link ShippingCostRule} and calls it. It cannot tell
 * which rule it is holding, has no branch that depends on the answer, and does
 * not change when a fifth rule is written.
 *
 * <p>That is the test of whether Strategy has actually been applied. Moving a
 * {@code switch} out of this class and into a helper would relocate the
 * decision; taking the behaviour as a constructor argument removes it.
 */
public final class CheckoutService {

    private final ShippingCostRule shippingRule;

    public CheckoutService(ShippingCostRule shippingRule) {
        this.shippingRule = Objects.requireNonNull(shippingRule, "shippingRule");
    }

    /**
     * Prices a shipment and returns the full quote.
     *
     * <p>The rule is asked exactly once. Calling it twice — say, once to
     * print and once to total — would be a live bug the day someone writes a
     * rule that is not free of side effects, which is why the contract on
     * {@link ShippingCostRule#costFor} forbids that.
     */
    public Quote quote(Shipment shipment) {
        Objects.requireNonNull(shipment, "shipment");
        Money delivery = shippingRule.costFor(shipment);
        return new Quote(shippingRule.name(), shipment.orderSubtotal(), delivery);
    }

    /** The rule in force, for display. */
    public String ruleName() {
        return shippingRule.name();
    }
}
