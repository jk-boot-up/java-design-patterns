package com.jk.explore.loadbalancing;

import java.util.List;

/**
 * Four acts, each sending the same twelve requests to the same three instances and
 * differing only in who gets asked.
 *
 * The cluster is deliberately uneven: two instances answer in 10ms and the third
 * takes 60ms, because it is on older hardware. Real clusters look like this far
 * more often than the diagrams admit.
 */
public final class LoadBalancingDemo {

    private static final String SKU = "SKU-1234";
    private static final int REQUESTS = 12;

    public static void main(String[] args) {
        System.out.println("Client-side load balancing: three Catalog instances, one slow");
        System.out.println();

        firstOnTheList();
        roundRobin();
        leastLatency();
        twoClientsEachTakingTurns();
    }

    /** Act 1: what you get by writing instances.get(0). */
    private static void firstOnTheList() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        CatalogCluster cluster = clusterOf(clock, log);

        new CatalogClient("Web", cluster, new FirstInstanceBalancer(), clock, log)
                .productName(SKU, REQUESTS);

        System.out.println("1. Always the first on the list");
        System.out.print(cluster.shareReport());
        System.out.printf("  %d requests took %dms in total%n",
                cluster.totalCalls(), log.elapsedMillis());
        System.out.println("  it is not slow -- catalog-1 happens to be a fast box. It is");
        System.out.println("  wasteful: the shop is paying for three instances and using one,");
        System.out.println("  and when catalog-1 falls over it takes every request with it.");
        System.out.println();
    }

    /** Act 2: take turns. Even, and even is not the same as fast. */
    private static void roundRobin() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        CatalogCluster cluster = clusterOf(clock, log);

        new CatalogClient("Web", cluster, new RoundRobinBalancer(), clock, log)
                .productName(SKU, REQUESTS);

        System.out.println("2. Round-robin: take turns");
        System.out.print(cluster.shareReport());
        System.out.printf("  %d requests took %dms in total%n",
                cluster.totalCalls(), log.elapsedMillis());
        System.out.println("  a perfectly even split, which sends a third of the shop's");
        System.out.println("  traffic to the slowest machine it owns.");
        System.out.println();
    }

    /** Act 3: measure, then prefer. */
    private static void leastLatency() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        CatalogCluster cluster = clusterOf(clock, log);

        LeastLatencyBalancer balancer = new LeastLatencyBalancer();
        new CatalogClient("Web", cluster, balancer, clock, log).productName(SKU, REQUESTS);

        System.out.println("3. Least latency: try each once, then prefer the fast ones");
        System.out.print(cluster.shareReport());
        System.out.printf("  %d requests took %dms in total%n",
                cluster.totalCalls(), log.elapsedMillis());
        System.out.printf("  the client now believes: catalog-1 %dms, catalog-2 %dms, catalog-3 %dms%n",
                balancer.believedLatency("catalog-1"),
                balancer.believedLatency("catalog-2"),
                balancer.believedLatency("catalog-3"));
        System.out.println("  it learned that on its own, from its own requests. Nothing told it.");
        System.out.println();
    }

    /**
     * Act 4: the honest cost of doing this in the client.
     *
     * Two clients, each taking perfect turns, each behaving impeccably. Between
     * them they leave a machine idle, because neither can see the other.
     */
    private static void twoClientsEachTakingTurns() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        CatalogCluster cluster = clusterOf(clock, log);

        CatalogClient web = new CatalogClient("Web", cluster, new RoundRobinBalancer(), clock, log);
        CatalogClient mobile = new CatalogClient("Mobile", cluster, new RoundRobinBalancer(), clock, log);
        web.productName(SKU, 2);
        mobile.productName(SKU, 2);

        System.out.println("4. Two clients, each taking perfect turns");
        System.out.print(cluster.shareReport());
        System.out.println("  each client did exactly the right thing on its own and they still");
        System.out.println("  left catalog-3 with nothing to do, because a client-side balancer");
        System.out.println("  can only balance the traffic it can see -- its own.");
        System.out.println();
        System.out.println("  If the callers are not yours to change, put one balancer in front of");
        System.out.println("  the cluster instead and let it see every request. That is simpler,");
        System.out.println("  and it is the right answer more often than this pattern's fans admit.");
    }

    private static CatalogCluster clusterOf(SimulatedClock clock, CallLog log) {
        CatalogCluster cluster = new CatalogCluster(clock, log);
        cluster.start("catalog-1", 10);
        cluster.start("catalog-2", 10);
        cluster.start("catalog-3", 60);   // older hardware, six times slower
        return cluster;
    }

    /** Kept so the tests can assert the cluster shape the demo uses. */
    static List<ServiceInstance> demoCluster() {
        return clusterOf(new SimulatedClock(), new CallLog(new SimulatedClock())).instances();
    }
}
