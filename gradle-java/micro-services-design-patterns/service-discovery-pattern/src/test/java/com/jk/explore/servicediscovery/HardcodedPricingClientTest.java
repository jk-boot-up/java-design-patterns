package com.jk.explore.servicediscovery;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

/**
 * The hardcoded address, and its costs pinned.
 *
 * These tests pass. The class is not broken — it returns the right price. What
 * these record is that it has no way to survive the set of instances changing,
 * which happens on every deployment.
 */
class HardcodedPricingClientTest {

    private static final String SKU = "SKU-1234";

    private ServiceRegistry registry;
    private PricingCluster cluster;
    private HardcodedPricingClient client;

    @BeforeEach
    void setUp() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        registry = new ServiceRegistry(clock, log);
        cluster = new PricingCluster(clock, log, registry);
        ServiceInstance one = cluster.start("pricing-1", 8081);
        cluster.start("pricing-2", 8082);
        cluster.start("pricing-3", 8083);
        client = new HardcodedPricingClient(cluster, one);
    }

    @Test
    void itWorksPerfectlyWhileNothingChanges() {
        assertEquals(Money.pence(44999), client.price(SKU));
        assertEquals(Money.pence(1850), client.price("SKU-2001"));
    }

    @Test
    void andAnOrdinaryDeploymentTakesItDown() {
        cluster.stop("pricing-1");

        assertThrows(ServiceUnavailableException.class, () -> client.price(SKU));
    }

    @Test
    void withTwoHealthyInstancesSittingIdle() {
        cluster.stop("pricing-1");

        assertThrows(ServiceUnavailableException.class, () -> client.price(SKU));

        assertEquals(2, registry.instances("Pricing").size(),
                "the capacity is there and paid for. The client cannot reach it, "
                        + "because it was told about one machine.");
    }

    @Test
    void andItCannotBeToldAboutAnyOther() {
        ServiceInstance two = new ServiceInstance("Pricing", "pricing-2", "10.0.1.82", 8082);

        assertThrows(IllegalArgumentException.class,
                () -> new HardcodedPricingClient(cluster, two),
                "the address is a constant. Changing it is a code change, a build "
                        + "and a deployment.");
    }
}
