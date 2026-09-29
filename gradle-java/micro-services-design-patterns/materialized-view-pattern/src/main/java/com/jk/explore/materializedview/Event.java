package com.jk.explore.materializedview;

/**
 * Something that happened in one of the services, published so others can react.
 */
public sealed interface Event {

    /** The orders service took an order. */
    record OrderPlaced(String orderId, String customerId, String productId, int quantity) implements Event {
    }

    /** The shipping service sent the parcel. */
    record OrderShipped(String orderId) implements Event {
    }

    /** The catalogue service gave a product a new name. */
    record ProductRenamed(String productId, String name) implements Event {
    }
}
