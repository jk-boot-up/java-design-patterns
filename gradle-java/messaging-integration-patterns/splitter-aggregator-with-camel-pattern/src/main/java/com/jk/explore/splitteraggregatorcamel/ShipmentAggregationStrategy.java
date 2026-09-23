package com.jk.explore.splitteraggregatorcamel;

import org.apache.camel.AggregationStrategy;
import org.apache.camel.Exchange;

/**
 * How two messages with the same order number are folded into one. Camel calls this for every shipment that
 * comes back. The first time it is called for an order there is nothing to fold into, so it starts a fresh
 * half-finished answer; every call after that adds the new shipment to the answer already being built.
 */
public class ShipmentAggregationStrategy implements AggregationStrategy {

    @Override
    public Exchange aggregate(Exchange existing, Exchange arriving) {
        Shipment shipment = arriving.getIn().getBody(Shipment.class);
        if (existing == null) {
            Gathering started = new Gathering(shipment.orderId(), shipment.of());
            started.add(shipment);
            arriving.getIn().setBody(started);
            return arriving;
        }
        existing.getIn().getBody(Gathering.class).add(shipment);
        return existing;
    }
}
