package com.jk.explore.strategyspring;

/** A fifth rule, added without touching {@link CheckoutService}. Not a component: the demo registers it. */
public class ExpressRule implements ShippingCostRule {
    @Override
    public long costFor(Shipment shipment) {
        return 999;
    }
}
