package com.jk.explore.servicediscovery;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The shared list of who is running right now.
 *
 * An instance announces itself when it starts, says "still here" every few
 * seconds, and is taken off the list when it stops. Callers ask this list for an
 * address instead of having one written into their code.
 *
 * <p>The interesting part of this class is not registration — that is a map. It
 * is the <strong>lease</strong>. A registration is only good for
 * {@link #LEASE_MILLIS} from its last heartbeat, because an instance that dies
 * badly cannot tell anybody it has gone. Without an expiry, one crashed process
 * would poison the list for ever. With an expiry, it poisons the list for a few
 * seconds, and that window is the honest cost of the pattern rather than a bug in
 * it.
 */
public final class ServiceRegistry {

    /** How long a registration is good for without a heartbeat. */
    public static final long LEASE_MILLIS = 3_000;

    private record Lease(ServiceInstance instance, long lastHeartbeatAt) { }

    private final SimulatedClock clock;
    private final CallLog log;
    private final Map<String, Lease> leases = new LinkedHashMap<>();

    public ServiceRegistry(SimulatedClock clock, CallLog log) {
        this.clock = clock;
        this.log = log;
    }

    /** An instance announcing itself as it starts up. */
    public void register(ServiceInstance instance) {
        leases.put(instance.instanceId(), new Lease(instance, clock.millis()));
        log.note("Registry", "REGISTER", instance.toString());
    }

    /** An instance saying "still here". Renews its lease. */
    public void heartbeat(String instanceId) {
        Lease lease = leases.get(instanceId);
        if (lease == null) {
            return;
        }
        leases.put(instanceId, new Lease(lease.instance(), clock.millis()));
    }

    /** An instance shutting down politely. Takes effect at once. */
    public void deregister(String instanceId) {
        if (leases.remove(instanceId) != null) {
            log.note("Registry", "DEREGISTER", instanceId + " left cleanly");
        }
    }

    /**
     * Everyone believed to be running, in registration order.
     *
     * "Believed" is doing real work in that sentence. An instance whose lease has
     * expired is dropped here, and an instance that died two seconds ago is still
     * in the answer.
     */
    public List<ServiceInstance> instances(String serviceName) {
        List<ServiceInstance> live = new ArrayList<>();
        List<String> expired = new ArrayList<>();
        for (Lease lease : leases.values()) {
            if (!lease.instance().serviceName().equals(serviceName)) {
                continue;
            }
            if (clock.millis() - lease.lastHeartbeatAt() > LEASE_MILLIS) {
                expired.add(lease.instance().instanceId());
            } else {
                live.add(lease.instance());
            }
        }
        for (String instanceId : expired) {
            leases.remove(instanceId);
            log.note("Registry", "EXPIRED", instanceId + " missed its heartbeats");
        }
        return live;
    }

    /** How many registrations are held, live or not yet expired. */
    public int size() {
        return leases.size();
    }
}
