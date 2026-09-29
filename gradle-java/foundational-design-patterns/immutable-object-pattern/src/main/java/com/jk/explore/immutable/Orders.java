package com.jk.explore.immutable;

/**
 * Placed orders that remember where to send the parcel, holding the address object they are handed.
 */
public final class Orders {

    /** Holds a mutable address: whoever else holds it can change where this parcel goes. */
    public record OldOrder(String id, MutableAddress shipTo) {
    }

    /** Holds an immutable address: fixed at the moment the order was placed. */
    public record Order(String id, Address shipTo) {
    }

    private Orders() {
    }
}
