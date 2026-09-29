package com.jk.explore.healthcheck;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Predicate;

/**
 * Shares orders between instances in turn, skipping any that its check says are not fit for work.
 */
public final class LoadBalancer {

    private final List<Instance> instances;
    private final Predicate<Instance> fit;

    public LoadBalancer(List<Instance> instances, Predicate<Instance> fit) {
        this.instances = instances;
        this.fit = fit;
    }

    /** Sends {@code n} orders round the instances that pass the check; returns how many failed. */
    public int send(int n) {
        List<Instance> pool = new ArrayList<>(instances.stream().filter(fit).toList());
        if (pool.isEmpty()) {
            return n;
        }
        int failed = 0;
        for (int k = 0; k < n; k++) {
            if (!pool.get(k % pool.size()).placeOrder()) {
                failed++;
            }
        }
        return failed;
    }

    public List<String> inRotation() {
        return instances.stream().filter(fit).map(Instance::name).toList();
    }
}
