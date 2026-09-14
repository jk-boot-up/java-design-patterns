package com.jk.explore.loadbalancing;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Prefer whichever instance has been fastest so far.
 *
 * This is the one that justifies doing the balancing in the client at all. "How
 * slow has this instance been for me?" is a question only the caller can answer —
 * it depends on which rack the caller is in, which network path the packets take,
 * and what the caller is asking for. A balancer sitting in the middle of the
 * network measures its own view, which is a different view.
 *
 * <p>It tries every instance once before it starts preferring, because a balancer
 * that trusts a measurement it has not taken is just round-robin with extra
 * confidence.
 */
public final class LeastLatencyBalancer implements LoadBalancer {

    private final Map<String, Long> averageMillis = new HashMap<>();
    private final Map<String, Integer> samples = new HashMap<>();

    @Override
    public ServiceInstance choose(List<ServiceInstance> candidates) {
        for (ServiceInstance candidate : candidates) {
            if (!averageMillis.containsKey(candidate.instanceId())) {
                return candidate;   // never tried; measure it before judging it
            }
        }
        return candidates.stream()
                .min((a, b) -> Long.compare(averageMillis.get(a.instanceId()),
                        averageMillis.get(b.instanceId())))
                .orElseThrow();
    }

    @Override
    public void observed(ServiceInstance instance, long tookMillis) {
        int seen = samples.merge(instance.instanceId(), 1, Integer::sum);
        long previous = averageMillis.getOrDefault(instance.instanceId(), tookMillis);
        // A running mean, so one slow request does not rewrite history.
        averageMillis.put(instance.instanceId(),
                previous + (tookMillis - previous) / seen);
    }

    /** What this client currently believes about an instance. */
    public long believedLatency(String instanceId) {
        return averageMillis.getOrDefault(instanceId, -1L);
    }

    @Override
    public String name() {
        return "least-latency";
    }
}
