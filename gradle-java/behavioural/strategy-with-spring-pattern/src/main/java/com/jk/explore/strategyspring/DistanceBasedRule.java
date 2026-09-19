package com.jk.explore.strategyspring;

import org.springframework.stereotype.Component;

/** A base fee plus fifty pence per hundred miles. */
@Component("distance")
public class DistanceBasedRule implements ShippingCostRule {
    @Override
    public long costFor(Shipment shipment) {
        return 299 + (shipment.miles() / 100) * 50;
    }
}
