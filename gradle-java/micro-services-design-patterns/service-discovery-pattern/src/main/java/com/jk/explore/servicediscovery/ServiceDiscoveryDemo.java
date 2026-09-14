package com.jk.explore.servicediscovery;

/**
 * Four acts. A deployment, a crash, and the few seconds in between when the
 * registry is confidently wrong.
 */
public final class ServiceDiscoveryDemo {

    private static final String SKU = "SKU-1234";

    public static void main(String[] args) {
        actOne();
        actTwo();
        actThree();
        actFour();
    }

    /** The hardcoded client, on the day pricing-1 is restarted. */
    private static void actOne() {
        heading("1. A hardcoded address, and a routine deployment");

        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        ServiceRegistry registry = new ServiceRegistry(clock, log);
        PricingCluster cluster = new PricingCluster(clock, log, registry);
        ServiceInstance one = cluster.start("pricing-1", 8081);
        cluster.start("pricing-2", 8082);
        cluster.start("pricing-3", 8083);

        HardcodedPricingClient client = new HardcodedPricingClient(cluster, one);
        System.out.printf("  before the deploy: %s%n", client.price(SKU));

        cluster.stop("pricing-1");
        try {
            client.price(SKU);
        } catch (ServiceUnavailableException e) {
            System.out.print(log.timeline());
            System.out.printf("  after the deploy:  %s%n", e.getMessage());
        }
        System.out.println("  two healthy instances are sitting idle. The client "
                + "cannot use them,");
        System.out.println("  because it was told about one machine and has no way "
                + "to learn about another.\n");
    }

    /** The same deployment, with discovery. */
    private static void actTwo() {
        heading("2. The same deployment, with a registry");

        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        ServiceRegistry registry = new ServiceRegistry(clock, log);
        PricingCluster cluster = new PricingCluster(clock, log, registry);
        cluster.start("pricing-1", 8081);
        cluster.start("pricing-2", 8082);
        cluster.start("pricing-3", 8083);

        DiscoveringPricingClient client =
                new DiscoveringPricingClient(registry, cluster, log);
        System.out.printf("  before the deploy: %s%n", client.price(SKU));

        cluster.stop("pricing-1");
        System.out.printf("  after the deploy:  %s%n", client.price(SKU));

        cluster.start("pricing-4", 8084);
        System.out.printf("  after scaling up:  %s%n", client.price(SKU));

        System.out.print(log.timeline());
        System.out.println("  no code changed, no restart, no configuration edit.\n");
    }

    /** The crash. The registry is wrong, and the client copes anyway. */
    private static void actThree() {
        heading("3. A crash: the registry is wrong for a few seconds");

        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        ServiceRegistry registry = new ServiceRegistry(clock, log);
        PricingCluster cluster = new PricingCluster(clock, log, registry);
        cluster.start("pricing-1", 8081);
        cluster.start("pricing-2", 8082);

        DiscoveringPricingClient client =
                new DiscoveringPricingClient(registry, cluster, log);

        // No deregistration: the process is simply gone.
        cluster.kill("pricing-1");

        System.out.printf("  price still answered: %s%n", client.price(SKU));
        System.out.print(log.timeline());
        System.out.printf("  the registry still lists %d instances, one of which "
                + "is dead.%n", registry.size());
        System.out.println("  a client that trusted the first address would have "
                + "failed here. This one");
        System.out.println("  tried the next name on the list.\n");
    }

    /** The lease expires and the list becomes true again. */
    private static void actFour() {
        heading("4. The lease expires and the list corrects itself");

        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        ServiceRegistry registry = new ServiceRegistry(clock, log);
        PricingCluster cluster = new PricingCluster(clock, log, registry);
        cluster.start("pricing-1", 8081);
        cluster.start("pricing-2", 8082);
        cluster.kill("pricing-1");

        System.out.printf("  immediately after the crash: %d listed%n",
                registry.instances("Pricing").size());

        // The survivors keep saying "still here"; the dead one cannot.
        for (int second = 1; second <= 4; second++) {
            clock.advance(1_000);
            cluster.heartbeatAll();
            System.out.printf("  %ds later: %d listed%n", second,
                    registry.instances("Pricing").size());
        }

        System.out.print(log.timeline());
        System.out.printf("  the lease is %dms, so the wrong answer lasted a few "
                + "seconds and then stopped.%n", ServiceRegistry.LEASE_MILLIS);
        System.out.println("  that window is the price of the pattern. It is not a "
                + "bug in it, and there is");
        System.out.println("  no setting that removes it — a shorter lease just "
                + "trades it for more traffic.");
    }

    private static void heading(String text) {
        System.out.println("=".repeat(66));
        System.out.println(text);
        System.out.println("=".repeat(66));
    }
}
