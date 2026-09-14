package com.jk.explore.servicediscovery;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * What only a registry gives you, and what it costs.
 *
 * A hardcoded address returns the right price too, so no test here is happy
 * about a price. These are about who the caller was able to reach, and when the
 * list it was reading from was wrong.
 */
class ServiceRegistryTest {

    private static final String SKU = "SKU-1234";

    private SimulatedClock clock;
    private CallLog log;
    private ServiceRegistry registry;
    private PricingCluster cluster;
    private DiscoveringPricingClient client;

    @BeforeEach
    void setUp() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
        registry = new ServiceRegistry(clock, log);
        cluster = new PricingCluster(clock, log, registry);
        client = new DiscoveringPricingClient(registry, cluster, log);
    }

    @Test
    void anInstanceIsReachableAsSoonAsItRegisters() {
        cluster.start("pricing-1", 8081);

        assertEquals(Money.pence(44999), client.price(SKU));
    }

    @Test
    void aNewInstanceIsFoundWithoutAnyCodeOrConfigurationChange() {
        cluster.start("pricing-1", 8081);
        client.price(SKU);

        cluster.start("pricing-2", 8082);

        assertEquals(2, registry.instances("Pricing").size(),
                "scaling up on Black Friday morning is not a deployment of the caller");
    }

    @Test
    void aPoliteShutdownRemovesTheInstanceImmediately() {
        cluster.start("pricing-1", 8081);
        cluster.start("pricing-2", 8082);

        cluster.stop("pricing-1");

        assertEquals(List.of("pricing-2"),
                registry.instances("Pricing").stream()
                        .map(ServiceInstance::instanceId).toList());
    }

    @Test
    void aCallerSurvivesTheInstanceItWasUsingBeingDeployed() {
        cluster.start("pricing-1", 8081);
        cluster.start("pricing-2", 8082);
        client.price(SKU);

        cluster.stop("pricing-1");

        assertEquals(Money.pence(44999), client.price(SKU),
                "the whole point: the set of instances changed and nothing broke");
    }

    @Test
    void aCrashedInstanceStaysOnTheListBecauseItCouldNotSaySoItself() {
        cluster.start("pricing-1", 8081);
        cluster.start("pricing-2", 8082);

        cluster.kill("pricing-1");

        assertEquals(2, registry.instances("Pricing").size(),
                "this is the honest cost of the pattern, not a bug in it: a registry "
                        + "cannot know about a death nobody reported");
    }

    @Test
    void aStaleEntryIsHandedOutAndTheClientCopesByTryingTheNextOne() {
        cluster.start("pricing-1", 8081);
        cluster.start("pricing-2", 8082);
        cluster.kill("pricing-1");

        assertEquals(Money.pence(44999), client.price(SKU));

        assertEquals(0, cluster.callsTo("pricing-1"));
        assertEquals(1, cluster.callsTo("pricing-2"));
        assertTrue(log.entries().stream().anyMatch(e -> "STALE".equals(e.outcome())),
                "the client noticed the list was wrong, and said so");
    }

    @Test
    void anExpiredLeaseIsDroppedOnTheNextLookup() {
        cluster.start("pricing-1", 8081);
        cluster.start("pricing-2", 8082);
        cluster.kill("pricing-1");

        clock.advance(ServiceRegistry.LEASE_MILLIS + 1);
        cluster.heartbeatAll();

        assertEquals(List.of("pricing-2"),
                registry.instances("Pricing").stream()
                        .map(ServiceInstance::instanceId).toList(),
                "the survivors renewed their leases; the dead one could not");
    }

    @Test
    void aLeaseIsStillGoodOnItsLastMillisecond() {
        cluster.start("pricing-1", 8081);
        cluster.kill("pricing-1");

        clock.advance(ServiceRegistry.LEASE_MILLIS);

        assertEquals(1, registry.instances("Pricing").size(),
                "expiry is strictly after the lease, so the boundary is not a guess");
    }

    @Test
    void heartbeatsKeepALiveInstanceOnTheList() {
        cluster.start("pricing-1", 8081);

        for (int second = 0; second < 10; second++) {
            clock.advance(1_000);
            cluster.heartbeatAll();
        }

        assertEquals(1, registry.instances("Pricing").size(),
                "ten seconds is more than three leases, and it is still there");
    }

    @Test
    void aHeartbeatFromSomethingNeverRegisteredIsIgnored() {
        registry.heartbeat("pricing-99");

        assertEquals(0, registry.size(),
                "a heartbeat renews a registration; it does not create one");
    }

    @Test
    void withNothingRegisteredTheCallerGetsAnHonestFailure() {
        ServiceUnavailableException failure = assertThrows(
                ServiceUnavailableException.class, () -> client.price(SKU));

        assertTrue(failure.getMessage().contains("nothing registered"));
    }

    @Test
    void whenEveryOfferedInstanceIsDeadTheCallerFailsRatherThanHanging() {
        cluster.start("pricing-1", 8081);
        cluster.start("pricing-2", 8082);
        cluster.kill("pricing-1");
        cluster.kill("pricing-2");

        assertThrows(ServiceUnavailableException.class, () -> client.price(SKU));

        assertEquals(2, log.entries().stream()
                        .filter(e -> "STALE".equals(e.outcome())).count(),
                "it worked down the whole list before giving up");
    }

    @Test
    void theRegistryIsConsultedOnEveryCallRatherThanOnce() {
        cluster.start("pricing-1", 8081);

        client.price(SKU);
        client.price("SKU-2001");
        client.price("SKU-2002");

        assertEquals(3, client.lookups(),
                "the answer to 'where is Pricing' changes minute to minute, so "
                        + "caching it is how you reinvent the hardcoded address");
    }

    @Test
    void everyInstanceGivesTheSameAnswerSoTheChoiceIsFree() {
        cluster.start("pricing-1", 8081);
        Money fromFirst = client.price(SKU);
        cluster.stop("pricing-1");
        cluster.start("pricing-2", 8082);

        assertEquals(fromFirst, client.price(SKU),
                "instances are interchangeable; if they were not, this pattern "
                        + "would not be safe");
    }
}
