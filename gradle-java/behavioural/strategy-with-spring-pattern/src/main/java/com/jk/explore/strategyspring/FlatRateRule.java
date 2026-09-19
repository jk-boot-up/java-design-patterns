package com.jk.explore.strategyspring;

import org.springframework.stereotype.Component;

/** The same charge on everything. */
@Component("flat")
public class FlatRateRule implements ShippingCostRule {
    @Override
    public long costFor(Shipment shipment) {
        return 499;
    }
}
