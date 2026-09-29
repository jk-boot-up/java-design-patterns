package com.jk.explore.contentenricher;

/**
 * The two services that receive orders: the warehouse packs them and the email service confirms them.
 *
 * <p>The thin versions look the customer up themselves; the enriched versions
 * read the details straight from the message.
 */
public final class Receivers {

    /** Warehouse that must ask the customer service where to send each parcel. */
    public static String packThin(OrderPlaced order, CustomerDirectory directory) {
        Customer c = directory.find(order.customerId()).orElseThrow();
        return "pack " + order.orderId() + " for " + c.address();
    }

    /** Email service that must ask the customer service for the name. */
    public static String emailThin(OrderPlaced order, CustomerDirectory directory) {
        Customer c = directory.find(order.customerId()).orElseThrow();
        return "email " + c.name();
    }

    public static String pack(EnrichedOrder order) {
        return "pack " + order.orderId() + " for " + order.address();
    }

    public static String email(EnrichedOrder order) {
        return "email " + order.name();
    }

    private Receivers() {
    }
}
