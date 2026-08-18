package com.jk.explore.abstractfactory;

import java.util.List;

public class AbstractFactoryDemo {

    public static void main(String[] args) {

        // Three markets, three postcodes in each market's own format.
        record Shipment(MarketFactory factory, String postcode) { }

        List<Shipment> shipments = List.of(
                new Shipment(new UkMarketFactory(), "EH1 1YZ"),
                new Shipment(new UsMarketFactory(), "10001"),
                new Shipment(new IndiaMarketFactory(), "560001"));

        for (Shipment shipment : shipments) {
            // One line picks the whole family. Everything after it is identical.
            CheckoutService checkout = new CheckoutService(shipment.factory());

            Order order = new Order("ORD-3001", "CUST-001", 120.00, shipment.postcode());
            Quote quote = checkout.quote(order);

            System.out.println("Quote: " + quote);
            System.out.println();
        }

        // The family is enforced: a British postcode cannot slip into the
        // American market, because the validator came from the same factory.
        CheckoutService us = new CheckoutService(new UsMarketFactory());
        try {
            us.quote(new Order("ORD-3002", "CUST-002", 120.00, "EH1 1YZ"));
        } catch (IllegalArgumentException e) {
            System.out.println("Rejected: " + e.getMessage());
        }
    }
}
