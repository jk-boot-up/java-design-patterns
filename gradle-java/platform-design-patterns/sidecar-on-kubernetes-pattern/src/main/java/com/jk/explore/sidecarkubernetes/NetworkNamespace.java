package com.jk.explore.sidecarkubernetes;

import java.util.HashMap;
import java.util.Map;

/**
 * <strong>One network stack: one set of ports, and one loopback.</strong> Every
 * container placed in a namespace listens on it, and any of them reaches any
 * other on {@code localhost}. A container in a different namespace cannot.
 */
public final class NetworkNamespace {

    private final String address;
    private final Map<Integer, Container> listeners = new HashMap<>();

    NetworkNamespace(String address) {
        this.address = address;
    }

    public String address() {
        return address;
    }

    void listen(int port, Container container) {
        listeners.put(port, container);
    }

    /** Whoever is listening on this port here, if they are running. */
    public boolean reachable(int port) {
        Container listener = listeners.get(port);
        return listener != null && listener.running();
    }
}
