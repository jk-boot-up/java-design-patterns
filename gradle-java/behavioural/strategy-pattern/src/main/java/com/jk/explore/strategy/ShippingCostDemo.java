package com.jk.explore.strategy;

import java.util.List;

/**
 * Runnable entry point.
 *
 * <p>The output is arranged to make the interaction visible rather than just
 * the answer. The same three shipments are priced under all four rules, so
 * you can read down a column and see one rule's character, or across a row
 * and see four rules disagreeing about the same parcel — which is the whole
 * argument for keeping them apart.
 */
public final class ShippingCostDemo {

    private static final List<Shipment> SHIPMENTS = List.of(
            new Shipment("Edinburgh", 0.4, 45, Money.pounds(18.00)),
            new Shipment("Cardiff", 6.5, 180, Money.pounds(64.00)),
            new Shipment("Inverness", 24.0, 560, Money.pounds(31.50)));

    public static void main(String[] args) {
        System.out.println("Four rules, priced against the same three shipments.");
        System.out.println();

        for (String key : ShippingRules.names()) {
            CheckoutService checkout = new CheckoutService(ShippingRules.byName(key));
            System.out.println("Rule \"" + key + "\" -> " + checkout.ruleName());
            for (Shipment shipment : SHIPMENTS) {
                System.out.println("  " + shipment);
                System.out.println("    " + checkout.quote(shipment));
            }
            System.out.println();
        }

        System.out.println("The client is the same object every time.");
        System.out.println("CheckoutService never asks which rule it is holding:");
        Shipment cardiff = SHIPMENTS.get(1);
        for (String key : ShippingRules.names()) {
            Quote quote = new CheckoutService(ShippingRules.byName(key)).quote(cardiff);
            System.out.printf("  %-14s delivery %s%n",
                    key, quote.isFreeDelivery() ? "FREE" : quote.delivery());
        }
        System.out.println();

        System.out.println("Swapping the rule at runtime changes the price, not the code:");
        Shipment light = SHIPMENTS.get(0);
        ShippingCostRule campaign = ShippingRules.byName("campaign");
        ShippingCostRule weight = ShippingRules.byName("weight");
        System.out.println("  " + new CheckoutService(weight).quote(light));
        System.out.println("  " + new CheckoutService(campaign).quote(light));
        System.out.println();

        System.out.println("An unknown rule name is refused, not defaulted:");
        try {
            ShippingRules.byName("second-class");
        } catch (IllegalArgumentException e) {
            System.out.println("  Rejected: " + e.getMessage());
        }
    }

    private ShippingCostDemo() {
    }
}
