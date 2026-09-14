package com.jk.explore.loadbalancing;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * The naive alternative, tested honestly.
 *
 * Every test in this class passes. That is deliberate and it is the lesson: a
 * concentration bug does not announce itself with a failure. It gives the right
 * answer, quickly, while quietly wasting two thirds of what the shop is paying
 * for and putting every request on one machine's shoulders.
 */
class FirstInstanceBalancerTest {

    private static final String SKU = "SKU-1234";

    private SimulatedClock clock;
    private CallLog log;
    private CatalogCluster cluster;

    @BeforeEach
    void startThreeInstances() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
        cluster = new CatalogCluster(clock, log);
        cluster.start("catalog-1", 10);
        cluster.start("catalog-2", 10);
        cluster.start("catalog-3", 60);
    }

    private CatalogClient naiveClient() {
        return new CatalogClient("Web", cluster, new FirstInstanceBalancer(), clock, log);
    }

    @Test
    @DisplayName("it returns the correct product name every time")
    void itIsNotWrong() {
        for (int i = 0; i < 5; i++) {
            assertEquals("Barista Pro Espresso Machine", naiveClient().productName(SKU));
        }
    }

    @Test
    @DisplayName("with one instance running it is indistinguishable from round-robin")
    void itLooksPerfectInTesting() {
        SimulatedClock soloClock = new SimulatedClock();
        CallLog soloLog = new CallLog(soloClock);
        CatalogCluster solo = new CatalogCluster(soloClock, soloLog);
        solo.start("catalog-1", 10);

        new CatalogClient("Web", solo, new FirstInstanceBalancer(), soloClock, soloLog)
                .productName(SKU, 5);

        assertEquals(5, solo.callsTo("catalog-1"));
    }

    @Test
    @DisplayName("in production it sends every request to one instance")
    void itConcentratesAllTraffic() {
        naiveClient().productName(SKU, 12);

        assertEquals(12, cluster.callsTo("catalog-1"));
        assertEquals(0, cluster.callsTo("catalog-2"));
        assertEquals(0, cluster.callsTo("catalog-3"));
    }

    @Test
    @DisplayName("it is not even slow, which is why nobody notices")
    void itIsFastOnThisCluster() {
        naiveClient().productName(SKU, 12);

        // Faster than round-robin's 320ms, because catalog-1 happens to be quick.
        assertEquals(120, log.elapsedMillis());
    }

    @Test
    @DisplayName("two idle instances cost the same money as the busy one")
    void theOtherTwoAreBoughtAndUnused() {
        naiveClient().productName(SKU, 12);

        long idle = cluster.instances().stream()
                .filter(i -> cluster.callsTo(i.instanceId()) == 0)
                .count();
        assertEquals(2, idle);
    }
}
