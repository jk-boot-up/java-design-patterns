package com.jk.explore.healthcheck;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", HealthEndpointDemo.run());

    @Test
    void openPortLosesOrders() {
        assertTrue(all.contains("in rotation [A, B, C]\n  9 orders sent: 3 failed"));
    }

    @Test
    void livenessRemovesAndRestarts() {
        assertTrue(all.contains("GET B/health/live: 503 DOWN (not responding)"));
        assertTrue(all.contains("in rotation [A, C]; 9 orders sent: 0 failed"));
        assertTrue(all.contains("B is restarted: now 200 UP, back in rotation [A, B, C]"));
    }

    @Test
    void readinessSeparatesDownFromDegraded() {
        assertTrue(all.contains("GET C/health/ready: 503 DOWN (database down, recommendations down)"));
        assertTrue(all.contains("GET A/health/ready: 200 DEGRADED (recommendations down)"));
        assertTrue(all.contains("in rotation [A, B]; 9 orders sent: 0 failed"));
    }

    @Test
    void deepLivenessRestartsEverything() {
        assertTrue(all.contains("checks payments too: 3 of 3 instances restarted"));
        assertTrue(all.contains("only the process: 0 restarted"));
    }

    @Test
    void checksCostCalls() {
        assertTrue(all.contains("54 dependency calls a minute"));
    }
}
