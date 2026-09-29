package com.jk.explore.eventcarried;

/**
 * The two kinds of event the customer service can publish.
 */
public final class Events {

    /** A thin notification: something changed, ask me what. */
    public record CustomerChanged(String customerId) {
    }

    /** Event-carried state: the new state travels in the event, with a version to order it. */
    public record AddressChanged(String customerId, Address address, int version) {
    }

    private Events() {
    }
}
