package com.jk.explore.servicediscovery;

/**
 * One running copy of a service, and where to reach it.
 *
 * Three instances of Pricing are three of these. They are interchangeable —
 * any of them can answer any question — which is exactly why a caller needs to
 * be told which ones exist rather than deciding for itself.
 */
public record ServiceInstance(String serviceName, String instanceId,
                              String host, int port) {

    public String address() {
        return host + ":" + port;
    }

    @Override
    public String toString() {
        return instanceId + " (" + address() + ")";
    }
}
