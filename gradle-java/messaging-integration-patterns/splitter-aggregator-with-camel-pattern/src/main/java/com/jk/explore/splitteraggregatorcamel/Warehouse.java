package com.jk.explore.splitteraggregatorcamel;

import org.apache.camel.Exchange;
import org.apache.camel.Processor;
import java.util.ArrayList;
import java.util.List;

/**
 * The step that stands in for a warehouse picking one line of a split order. It turns the line into a priced
 * shipment that still carries the order number and its place in the order, and it records every thread it was
 * ever called on, which is how the demo shows that one picker did all the work in the first act.
 */
public class Warehouse implements Processor {

    private final List<String> threads = new ArrayList<>();

    @Override
    public void process(Exchange exchange) {
        OrderLine line = exchange.getIn().getBody(OrderLine.class);
        String orderId = exchange.getIn().getHeader("orderId", String.class);
        int index = exchange.getIn().getHeader("shipmentIndex", Integer.class);
        int of = exchange.getIn().getHeader("shipmentCount", Integer.class);
        synchronized (threads) {
            String name = Thread.currentThread().getName();
            if (!threads.contains(name)) {
                threads.add(name);
            }
        }
        exchange.getIn().setHeader("warehouse", line.warehouse());
        exchange.getIn().setBody(new Shipment(orderId, index, of, line.warehouse(), line.describe(), line.linePence()));
    }

    /** How many different threads ever did the picking. */
    public int threadsUsed() {
        synchronized (threads) {
            return threads.size();
        }
    }
}
