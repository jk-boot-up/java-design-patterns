package com.jk.explore.strategyspring;

import org.springframework.stereotype.Component;

/** A band table by weight. */
@Component("weightBanded")
public class WeightBandedRule implements ShippingCostRule {
    @Override
    public long costFor(Shipment shipment) {
        if (shipment.weightGrams() <= 500) {
            return 299;
        }
        return shipment.weightGrams() <= 2000 ? 499 : 899;
    }
}
