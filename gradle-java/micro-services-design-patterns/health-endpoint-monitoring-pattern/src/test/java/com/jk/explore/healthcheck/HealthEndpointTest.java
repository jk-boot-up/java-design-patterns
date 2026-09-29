package com.jk.explore.healthcheck;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class HealthEndpointTest {

    private final Dependency db = new Dependency("database", true);
    private final Dependency recs = new Dependency("recommendations", false);
    private final Instance i = new Instance("A", List.of(db, recs));

    @Test
    void healthyInstanceIsUp() {
        assertEquals("200 UP", HealthEndpoint.ready(i).toString());
        assertEquals("200 UP", HealthEndpoint.live(i).toString());
    }

    @Test
    void stuckInstanceFailsBoth() {
        i.setStuck(true);
        assertEquals(503, HealthEndpoint.live(i).code());
        assertEquals(503, HealthEndpoint.ready(i).code());
    }

    @Test
    void criticalDependencyDownIsNotReadyButAlive() {
        db.setUp(false);
        assertEquals("503 DOWN (database down)", HealthEndpoint.ready(i).toString());
        assertEquals(200, HealthEndpoint.live(i).code());
    }

    @Test
    void nonCriticalDependencyDownIsDegraded() {
        recs.setUp(false);
        assertEquals("200 DEGRADED (recommendations down)", HealthEndpoint.ready(i).toString());
    }

    @Test
    void restarterWaitsForThreeFailures() {
        i.setStuck(true);
        Restarter r = new Restarter(HealthEndpoint::live);
        r.checkAll(List.of(i));
        r.checkAll(List.of(i));
        assertEquals(0, i.restarts());
        r.checkAll(List.of(i));
        assertEquals(1, i.restarts());
        assertEquals(200, HealthEndpoint.live(i).code());
    }

    @Test
    void loadBalancerSkipsUnreadyInstances() {
        Instance b = new Instance("B", List.of(new Dependency("database", true)));
        b.setStuck(true);
        LoadBalancer lb = new LoadBalancer(List.of(i, b), x -> HealthEndpoint.ready(x).code() == 200);
        assertEquals(List.of("A"), lb.inRotation());
        assertEquals(0, lb.send(4));
    }
}
