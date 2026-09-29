package com.jk.explore.eventcarried;

import java.util.HashMap;
import java.util.Map;

/**
 * The pattern: shipping keeps its own copy of the addresses it needs, filled from the events,
 * and never calls the customer service.
 */
public final class ReplicaShipping {

    private final Map<String, Events.AddressChanged> copy = new HashMap<>();
    private final boolean checkVersions;

    public ReplicaShipping(boolean checkVersions) {
        this.checkVersions = checkVersions;
    }

    public void on(Events.AddressChanged event) {
        Events.AddressChanged held = copy.get(event.customerId());
        if (checkVersions && held != null && held.version() >= event.version()) {
            return;   // an older event arriving late: ignore it
        }
        copy.put(event.customerId(), event);
    }

    public String label(String orderId, String customerId) {
        Events.AddressChanged held = copy.get(customerId);
        return held == null ? null : orderId + " -> " + held.address();
    }

    public int copies() {
        return copy.size();
    }
}
