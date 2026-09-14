package com.jk.explore.loadbalancing;

import java.util.List;

/**
 * The caller. One of possibly many, each with its own balancer.
 *
 * Notice how little there is here. The client asks the cluster who is available,
 * hands that list to whatever balancer it was given, calls the winner, and reports
 * back how long it took. It contains no policy at all — swapping round-robin for
 * least-latency changes nothing in this file, which is exactly the property
 * Strategy exists to give you.
 */
public final class CatalogClient {

    private final String clientName;
    private final CatalogCluster cluster;
    private final LoadBalancer balancer;
    private final SimulatedClock clock;
    private final CallLog log;

    public CatalogClient(String clientName, CatalogCluster cluster, LoadBalancer balancer,
                         SimulatedClock clock, CallLog log) {
        this.clientName = clientName;
        this.cluster = cluster;
        this.balancer = balancer;
        this.clock = clock;
        this.log = log;
    }

    /** Fetches one product name, choosing an instance to ask. */
    public String productName(String sku) {
        List<ServiceInstance> candidates = cluster.instances();
        ServiceInstance chosen = balancer.choose(candidates);
        log.note(clientName, "CHOSE", chosen.instanceId() + " by " + balancer.name());

        long startedAt = clock.millis();
        String name = cluster.call(chosen, sku);
        balancer.observed(chosen, clock.millis() - startedAt);
        return name;
    }

    /** Fetches the same product repeatedly, which is how a share of traffic is built. */
    public void productName(String sku, int times) {
        for (int i = 0; i < times; i++) {
            productName(sku);
        }
    }

    public String clientName() {
        return clientName;
    }

    public LoadBalancer balancer() {
        return balancer;
    }
}
