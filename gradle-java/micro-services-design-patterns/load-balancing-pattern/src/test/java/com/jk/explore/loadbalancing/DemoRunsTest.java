package com.jk.explore.loadbalancing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;

/** The demo is part of the teaching material, so it is kept working by a test. */
class DemoRunsTest {

    @Test
    @DisplayName("the demo runs all four acts without throwing")
    void demoRuns() {
        assertDoesNotThrow(() -> LoadBalancingDemo.main(new String[0]));
    }

    @Test
    @DisplayName("the demo cluster is three instances, one of them six times slower")
    void demoClusterIsUneven() {
        assertEquals(3, LoadBalancingDemo.demoCluster().size());
        assertEquals(60, LoadBalancingDemo.demoCluster().get(2).latencyMillis());
    }
}
