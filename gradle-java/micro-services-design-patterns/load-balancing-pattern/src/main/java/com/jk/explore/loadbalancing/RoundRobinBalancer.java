package com.jk.explore.loadbalancing;

import java.util.List;

/**
 * Take turns. The default answer, and usually the right one.
 *
 * It needs no measurements, no configuration and no knowledge of anything, and it
 * spreads load exactly evenly. Its one weakness is that "evenly" is not the same
 * as "well": if one instance is three times slower than the others, round-robin
 * cheerfully sends it a third of the traffic anyway.
 */
public final class RoundRobinBalancer implements LoadBalancer {

    private int next;

    @Override
    public ServiceInstance choose(List<ServiceInstance> candidates) {
        // The counter is per client, and that is the whole story of this pattern's
        // weakness: two clients each take perfect turns and know nothing of each
        // other.
        ServiceInstance chosen = candidates.get(Math.floorMod(next, candidates.size()));
        next++;
        return chosen;
    }

    @Override
    public String name() {
        return "round-robin";
    }
}
