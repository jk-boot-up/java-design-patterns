package com.jk.explore.builder;

import java.util.List;

/**
 * Fixed recipes built on top of {@link PurchaseOrder.Builder}.
 *
 * <p>The classic Gang of Four description of this pattern has a fourth
 * role — a <em>Director</em> — that runs a builder through a fixed
 * sequence of steps so callers do not have to know the recipe themselves.
 * Java rarely writes that as its own class hierarchy; a static method that
 * drives the builder does the same job with far less ceremony, and this
 * class is that method, three times over.
 *
 * <p>Notice what every preset here has in common: none of them talks to
 * {@code PurchaseOrder}'s fields, its constructor, or {@code List.copyOf}.
 * They only ever call methods on {@link PurchaseOrder.Builder}. The
 * director depends on the builder's interface, never on the product's
 * internals — which is exactly why {@link PurchaseOrder} is free to change
 * its private representation without touching a single preset.
 */
public final class PurchaseOrderPresets {

    private PurchaseOrderPresets() {
    }

    /** Gift-wrapped, with a message, sent standard speed. */
    public static PurchaseOrder giftOrder(String orderId, String customerId,
                                          List<LineItem> items, Address address, String message) {
        PurchaseOrder.Builder builder = PurchaseOrder.builder(orderId, customerId)
                .shippingAddress(address)
                .giftMessage(message);
        items.forEach(builder::addItem);
        return builder.build();
    }

    /** No frills: the items, the address, nothing else switched on. */
    public static PurchaseOrder standardOrder(String orderId, String customerId,
                                              List<LineItem> items, Address address) {
        PurchaseOrder.Builder builder = PurchaseOrder.builder(orderId, customerId)
                .shippingAddress(address);
        items.forEach(builder::addItem);
        return builder.build();
    }

    /** Priority shipping, and a warehouse note asking for it to go out same-day. */
    public static PurchaseOrder expressOrder(String orderId, String customerId,
                                             List<LineItem> items, Address address) {
        PurchaseOrder.Builder builder = PurchaseOrder.builder(orderId, customerId)
                .shippingAddress(address)
                .priority()
                .notes("Ship same-day if received before 2pm.");
        items.forEach(builder::addItem);
        return builder.build();
    }
}
