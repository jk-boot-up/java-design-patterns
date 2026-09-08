package com.jk.explore.observer;

import java.util.Objects;

/**
 * What happened, as a value.
 *
 * <p>This is the whole of the contract between the order and everything that
 * reacts to it. Listeners get an {@code OrderEvent} and nothing else -- no
 * reference back to the {@link Order}, no way to ask it a follow-up question,
 * no way to change it. That is deliberate: a listener that can reach back into
 * the publisher is a listener that can change the publisher's state halfway
 * through a notification, and then the order of the listeners starts to matter.
 *
 * <p>It also carries no timestamp. A real system would want one; leaving it out
 * keeps the demo's output byte-for-byte identical on every run, which is what
 * lets the README quote it.
 */
public record OrderEvent(String orderId, OrderStatus from, OrderStatus to) {

    public OrderEvent {
        Objects.requireNonNull(orderId, "orderId");
        Objects.requireNonNull(from, "from");
        Objects.requireNonNull(to, "to");
    }

    /** A one-line description, used by the listeners that log. */
    public String describe() {
        return orderId + ": " + from.label() + " -> " + to.label();
    }
}
