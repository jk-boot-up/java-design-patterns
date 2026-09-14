package com.jk.explore.loadbalancing;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The three running copies of the Catalog service, and a tally of who called
 * whom.
 *
 * In a real shop these would be three containers behind three addresses. Here they
 * are three {@link RemoteCall}s over the same in-memory function, differing only
 * in how long they take to answer. The tally — {@link #callsTo} — is the thing the
 * tests assert on, because the question this pattern answers is not "did I get the
 * right product name" (every instance gives that) but "how was the work shared
 * out".
 */
public final class CatalogCluster {

    private final Map<String, RemoteCall<String, String>> endpoints = new LinkedHashMap<>();
    private final Map<String, Integer> calls = new LinkedHashMap<>();
    private final List<ServiceInstance> instances = new ArrayList<>();

    private final SimulatedClock clock;
    private final CallLog log;

    public CatalogCluster(SimulatedClock clock, CallLog log) {
        this.clock = clock;
        this.log = log;
    }

    /**
     * Adds an instance to the cluster.
     *
     * @param instanceId the name that will appear in the timeline
     * @param latencyMillis how long this box takes to answer
     */
    public ServiceInstance start(String instanceId, long latencyMillis) {
        ServiceInstance instance = new ServiceInstance(instanceId, latencyMillis);
        instances.add(instance);
        calls.put(instanceId, 0);
        endpoints.put(instanceId, new RemoteCall<>(instanceId, latencyMillis,
                sku -> CatalogService.productName(sku), clock, log));
        return instance;
    }

    /** Every instance a client could choose from. Order is registration order. */
    public List<ServiceInstance> instances() {
        return List.copyOf(instances);
    }

    /** Sends one request to one instance and returns the product name. */
    public String call(ServiceInstance instance, String sku) {
        calls.merge(instance.instanceId(), 1, Integer::sum);
        return endpoints.get(instance.instanceId()).invoke(sku);
    }

    /** How many requests this instance has been sent. */
    public int callsTo(String instanceId) {
        return calls.getOrDefault(instanceId, 0);
    }

    /** How many requests the whole cluster has been sent. */
    public int totalCalls() {
        return calls.values().stream().mapToInt(Integer::intValue).sum();
    }

    /**
     * The share of traffic each instance received, in registration order.
     *
     * Printed by the demo, because a row of counts is the clearest possible
     * statement of what a balancer did.
     */
    public String shareReport() {
        StringBuilder out = new StringBuilder();
        for (ServiceInstance instance : instances) {
            int count = callsTo(instance.instanceId());
            int percent = totalCalls() == 0 ? 0 : (count * 100) / totalCalls();
            out.append(String.format("    %-10s %3d requests (%2d%%)  %3dms each%n",
                    instance.instanceId(), count, percent, instance.latencyMillis()));
        }
        return out.toString();
    }
}
