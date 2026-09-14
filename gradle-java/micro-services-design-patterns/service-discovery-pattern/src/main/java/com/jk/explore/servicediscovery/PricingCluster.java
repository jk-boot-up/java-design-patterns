package com.jk.explore.servicediscovery;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * The Pricing service, running as several instances.
 *
 * All instances answer the same questions with the same answers, because they
 * are the same program. What differs is whether a given one is running, and that
 * is what the whole project is about.
 *
 * <p>{@link #kill(String)} stops an instance the way a crash does: abruptly, with
 * no chance to tell the registry. {@link #stop(String)} stops one the way a
 * deployment does, politely. The difference between those two is the difference
 * between a stale entry and a clean one.
 */
public final class PricingCluster {

    private static final Map<String, Long> PRICES = Map.of(
            "SKU-1234", 44999L, "SKU-2001", 1850L, "SKU-2002", 1299L);

    private final SimulatedClock clock;
    private final CallLog log;
    private final ServiceRegistry registry;
    private final Set<String> running = new HashSet<>();
    private final Map<String, Integer> callsPerInstance = new HashMap<>();

    public PricingCluster(SimulatedClock clock, CallLog log, ServiceRegistry registry) {
        this.clock = clock;
        this.log = log;
        this.registry = registry;
    }

    /** Starts an instance and lets the registry know. */
    public ServiceInstance start(String instanceId, int port) {
        ServiceInstance instance = new ServiceInstance("Pricing", instanceId,
                "10.0.1." + port % 256, port);
        running.add(instanceId);
        registry.register(instance);
        return instance;
    }

    /** A crash. The process is gone and the registry has not been told. */
    public void kill(String instanceId) {
        running.remove(instanceId);
        log.note("Pricing", "CRASHED", instanceId + " died without deregistering");
    }

    /** A rolling deployment. The instance deregisters on the way out. */
    public void stop(String instanceId) {
        running.remove(instanceId);
        registry.deregister(instanceId);
    }

    /** Every running instance sends its heartbeat. */
    public void heartbeatAll() {
        running.forEach(registry::heartbeat);
    }

    /** A price call to one named instance, over the network. */
    public RemoteCall<String, Money> endpoint(ServiceInstance instance) {
        return new RemoteCall<>(instance.instanceId(), 10, sku -> {
            if (!running.contains(instance.instanceId())) {
                // The address in the registry still resolves; nothing is
                // listening at the other end of it.
                throw new ServiceUnavailableException(instance.instanceId());
            }
            callsPerInstance.merge(instance.instanceId(), 1, Integer::sum);
            return Money.pence(PRICES.getOrDefault(sku, 0L));
        }, clock, log);
    }

    public boolean isRunning(String instanceId) {
        return running.contains(instanceId);
    }

    public int callsTo(String instanceId) {
        return callsPerInstance.getOrDefault(instanceId, 0);
    }
}
