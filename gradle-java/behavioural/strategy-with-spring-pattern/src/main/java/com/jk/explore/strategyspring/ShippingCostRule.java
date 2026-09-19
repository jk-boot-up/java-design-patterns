package com.jk.explore.strategyspring;

/** The strategy: one pricing policy for delivery. */
public interface ShippingCostRule {
    long costFor(Shipment shipment);
}
