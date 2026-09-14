package com.jk.explore.loadbalancing;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * What a balancer must do, asserted as a property rather than as an answer.
 *
 * Every instance returns the same product name, so "the answer was right" proves
 * nothing here. What these tests pin down is the shape of the traffic: who got how
 * much, in what order, and what it cost.
 */
class LoadBalancerTest {

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

    private CatalogClient clientWith(LoadBalancer balancer) {
        return new CatalogClient("Web", cluster, balancer, clock, log);
    }

    // ---------------------------------------------------------------- the point

    @Test
    @DisplayName("every instance gives the same answer, which is why choosing is allowed")
    void instancesAreInterchangeable() {
        for (ServiceInstance instance : cluster.instances()) {
            assertEquals("Barista Pro Espresso Machine", cluster.call(instance, SKU));
        }
    }

    @Test
    @DisplayName("round-robin splits twelve requests evenly across three instances")
    void roundRobinSpreadsEvenly() {
        clientWith(new RoundRobinBalancer()).productName(SKU, 12);

        assertEquals(4, cluster.callsTo("catalog-1"));
        assertEquals(4, cluster.callsTo("catalog-2"));
        assertEquals(4, cluster.callsTo("catalog-3"));
    }

    @Test
    @DisplayName("round-robin visits each instance once before repeating any")
    void roundRobinTakesTurnsInOrder() {
        LoadBalancer balancer = new RoundRobinBalancer();
        List<ServiceInstance> candidates = cluster.instances();

        Set<String> firstThree = new HashSet<>();
        for (int i = 0; i < 3; i++) {
            firstThree.add(balancer.choose(candidates).instanceId());
        }

        assertEquals(3, firstThree.size());
        assertEquals("catalog-1", balancer.choose(candidates).instanceId());
    }

    @Test
    @DisplayName("an even split still sends a third of the traffic to the slowest box")
    void evenIsNotTheSameAsFast() {
        clientWith(new RoundRobinBalancer()).productName(SKU, 12);

        // 4 x 10ms + 4 x 10ms + 4 x 60ms
        assertEquals(320, log.elapsedMillis());
    }

    @Test
    @DisplayName("least-latency finishes the same twelve requests in far less time")
    void leastLatencyBeatsRoundRobinOnTime() {
        clientWith(new LeastLatencyBalancer()).productName(SKU, 12);

        // three probes (10 + 10 + 60) then nine fast calls
        assertEquals(170, log.elapsedMillis());
        assertTrue(log.elapsedMillis() < 320,
                "least-latency should beat round-robin's 320ms on this cluster");
    }

    @Test
    @DisplayName("least-latency tries every instance once before it prefers any")
    void leastLatencyMeasuresBeforeItJudges() {
        clientWith(new LeastLatencyBalancer()).productName(SKU, 3);

        assertEquals(1, cluster.callsTo("catalog-1"));
        assertEquals(1, cluster.callsTo("catalog-2"));
        assertEquals(1, cluster.callsTo("catalog-3"));
    }

    @Test
    @DisplayName("least-latency sends the slow instance one request and no more")
    void leastLatencyStopsUsingTheSlowInstance() {
        clientWith(new LeastLatencyBalancer()).productName(SKU, 12);

        assertEquals(1, cluster.callsTo("catalog-3"));
        assertEquals(11, cluster.callsTo("catalog-1") + cluster.callsTo("catalog-2"));
    }

    @Test
    @DisplayName("the client works out the latencies itself, from its own requests")
    void theClientLearnsWithoutBeingTold() {
        LeastLatencyBalancer balancer = new LeastLatencyBalancer();

        assertEquals(-1L, balancer.believedLatency("catalog-3"));

        clientWith(balancer).productName(SKU, 3);

        assertEquals(10L, balancer.believedLatency("catalog-1"));
        assertEquals(10L, balancer.believedLatency("catalog-2"));
        assertEquals(60L, balancer.believedLatency("catalog-3"));
    }

    @Test
    @DisplayName("a seeded random balancer is reproducible, and uses more than one instance")
    void randomIsSpreadOutAndRepeatable() {
        clientWith(new RandomBalancer(42L)).productName(SKU, 30);

        long used = cluster.instances().stream()
                .filter(i -> cluster.callsTo(i.instanceId()) > 0)
                .count();
        assertEquals(3, used);
        assertEquals(30, cluster.totalCalls());

        // The same seed makes the same choices, so this is a test and not a coin toss.
        LoadBalancer a = new RandomBalancer(42L);
        LoadBalancer b = new RandomBalancer(42L);
        for (int i = 0; i < 10; i++) {
            assertEquals(a.choose(cluster.instances()), b.choose(cluster.instances()));
        }
    }

    @Test
    @DisplayName("swapping the balancer changes nothing in the client")
    void theClientHoldsNoPolicy() {
        clientWith(new RoundRobinBalancer()).productName(SKU, 3);
        int spreadOut = (int) cluster.instances().stream()
                .filter(i -> cluster.callsTo(i.instanceId()) > 0).count();

        startThreeInstances();
        clientWith(new FirstInstanceBalancer()).productName(SKU, 3);
        int concentrated = (int) cluster.instances().stream()
                .filter(i -> cluster.callsTo(i.instanceId()) > 0).count();

        assertEquals(3, spreadOut);
        assertEquals(1, concentrated);
        assertNotEquals(spreadOut, concentrated);
    }

    @Test
    @DisplayName("the choice is made again on every single request")
    void everyRequestIsChosenAfresh() {
        clientWith(new RoundRobinBalancer()).productName(SKU, 6);

        assertEquals(6, log.countFor("Web"));   // one CHOSE note per request
    }

    // ----------------------------------------------------- the honest weakness

    @Test
    @DisplayName("two clients each taking perfect turns can still leave an instance idle")
    void independentClientsMakeCollectivelyBadChoices() {
        CatalogClient web = clientWith(new RoundRobinBalancer());
        CatalogClient mobile = clientWith(new RoundRobinBalancer());

        web.productName(SKU, 2);
        mobile.productName(SKU, 2);

        assertEquals(2, cluster.callsTo("catalog-1"));
        assertEquals(2, cluster.callsTo("catalog-2"));
        assertEquals(0, cluster.callsTo("catalog-3"),
                "neither client did anything wrong, and catalog-3 got nothing");
    }

    @Test
    @DisplayName("each client keeps its own turn counter, so both start at the same instance")
    void balancerStateIsPerClient() {
        LoadBalancer web = new RoundRobinBalancer();
        LoadBalancer mobile = new RoundRobinBalancer();

        assertEquals(web.choose(cluster.instances()), mobile.choose(cluster.instances()));
    }

    @Test
    @DisplayName("round-robin ignores how fast an instance was, and is allowed to")
    void roundRobinDoesNotHaveToPretendToLearn() {
        LoadBalancer balancer = new RoundRobinBalancer();
        List<ServiceInstance> candidates = cluster.instances();

        balancer.observed(candidates.get(2), 60);
        balancer.observed(candidates.get(2), 60);

        // Still takes its turns; the feedback changed nothing.
        assertEquals("catalog-1", balancer.choose(candidates).instanceId());
        assertEquals("catalog-2", balancer.choose(candidates).instanceId());
    }
}
