package com.jk.explore.loadbalancing;

import java.util.List;
import java.util.Random;

/**
 * Pick one at random.
 *
 * Worse than round-robin over a small number of requests and indistinguishable
 * from it over a large one, with one real advantage: it keeps no state, so a
 * thousand clients starting at once do not all begin with the same instance.
 *
 * <p>The {@link Random} is seeded from the constructor, which is not a detail. An
 * unseeded random balancer cannot be tested — the assertion would be about luck.
 * Seeding it means the demo and the tests get the identical sequence every time.
 */
public final class RandomBalancer implements LoadBalancer {

    private final Random random;

    public RandomBalancer(long seed) {
        this.random = new Random(seed);
    }

    @Override
    public ServiceInstance choose(List<ServiceInstance> candidates) {
        return candidates.get(random.nextInt(candidates.size()));
    }

    @Override
    public String name() {
        return "random";
    }
}
