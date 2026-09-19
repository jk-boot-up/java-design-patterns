package com.jk.explore.strategyspring;

/** Asks for the interface itself, which only works when exactly one rule qualifies. */
public class NeedsOneRule {

    private final ShippingCostRule rule;

    public NeedsOneRule(ShippingCostRule rule) {
        this.rule = rule;
    }

    public long cost(Shipment shipment) {
        return rule.costFor(shipment);
    }
}
