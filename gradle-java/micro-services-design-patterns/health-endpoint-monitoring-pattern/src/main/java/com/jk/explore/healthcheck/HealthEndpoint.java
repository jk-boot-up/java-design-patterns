package com.jk.explore.healthcheck;

import java.util.ArrayList;
import java.util.List;

/**
 * The pattern: two addresses an instance answers so others can tell whether to restart it or send it work.
 *
 * <p>{@code /health/live} asks only "is this process working at all?". If not,
 * restarting it may help. {@code /health/ready} also checks the dependencies:
 * a critical one down means "do not send me orders" (503), a non-critical one
 * down means "I can work, but with less" (200, DEGRADED).
 */
public final class HealthEndpoint {

    /** GET /health/live: shallow, never checks shared dependencies. */
    public static Health live(Instance i) {
        return i.stuck() ? new Health(503, "DOWN", "not responding") : new Health(200, "UP", "");
    }

    /** GET /health/ready: is it worth sending this instance an order right now? */
    public static Health ready(Instance i) {
        if (i.stuck()) {
            return new Health(503, "DOWN", "not responding");
        }
        List<String> down = new ArrayList<>();
        boolean criticalDown = false;
        for (Dependency d : i.dependencies()) {
            if (!d.check()) {
                down.add(d.name() + " down");
                criticalDown |= d.critical();
            }
        }
        if (criticalDown) {
            return new Health(503, "DOWN", String.join(", ", down));
        }
        return down.isEmpty() ? new Health(200, "UP", "") : new Health(200, "DEGRADED", String.join(", ", down));
    }

    /** The mistake: a liveness check that includes shared dependencies. */
    public static Health deepLive(Instance i) {
        Health r = ready(i);
        return r.code() == 503 ? r : new Health(200, "UP", "");
    }

    private HealthEndpoint() {
    }
}
