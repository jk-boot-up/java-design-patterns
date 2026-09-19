package com.jk.explore.strategyspring;

import org.springframework.stereotype.Component;

/** Free delivery on orders of fifty pounds or more. */
@Component("freeOverThreshold")
public class FreeOverThresholdRule implements ShippingCostRule {
    @Override
    public long costFor(Shipment shipment) {
        return shipment.orderTotalPence() >= 5000 ? 0 : 499;
    }
}
