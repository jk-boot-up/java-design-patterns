package com.jk.explore.healthcheck;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

/**
 * The platform's watchdog: restarts an instance after three failed liveness checks in a row.
 */
public final class Restarter {

    public static final int FAILURES_BEFORE_RESTART = 3;

    private final Function<Instance, Health> liveness;
    private final Map<Instance, Integer> failures = new HashMap<>();

    public Restarter(Function<Instance, Health> liveness) {
        this.liveness = liveness;
    }

    /** One round of checks, every 10 seconds on a real platform. */
    public void checkAll(List<Instance> instances) {
        for (Instance i : instances) {
            if (liveness.apply(i).code() == 200) {
                failures.put(i, 0);
            } else if (failures.merge(i, 1, Integer::sum) >= FAILURES_BEFORE_RESTART) {
                i.restart();
                failures.put(i, 0);
            }
        }
    }
}
