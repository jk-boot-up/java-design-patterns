package com.jk.explore.discoveryconsul;

import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class DiscoveryTest {

    @BeforeAll
    static void needConsul() {
        Assumptions.assumeTrue(ConsulAgent.available(), "consul is not on the PATH");
    }

    private static Cluster three() throws Exception {
        Cluster c = new Cluster();
        c.start("pricing-1");
        c.start("pricing-2", "10s");
        c.start("pricing-3");
        assertTrue(c.awaitListed(3));
        return c;
    }

    @Test
    void copiesRegisterThemselvesAndRequestsAreSpreadByName() throws Exception {
        try (Cluster c = three()) {
            assertEquals(List.of("pricing-1", "pricing-2", "pricing-3"), c.listed());
            assertEquals(Map.of("pricing-1", 2, "pricing-2", 2, "pricing-3", 2), c.send(6));
        }
    }

    @Test
    void aDeploymentBreaksAHardcodedAddressButNotAName() throws Exception {
        try (Cluster c = three()) {
            String old = c.baseUrl("pricing-1");
            c.stop("pricing-1");
            c.start("pricing-1");
            assertTrue(c.awaitListed(3));
            assertThrows(RuntimeException.class, () -> c.pricing.priceAt(old, "X"));
            assertEquals(Map.of("pricing-1", 2, "pricing-2", 2, "pricing-3", 2), c.send(6));
        }
    }

    @Test
    void aGracefulStopIsImmediateAndACrashIsStaleUntilTheCheckFails() throws Exception {
        try (Cluster c = three()) {
            c.stop("pricing-3");
            assertEquals(List.of("pricing-1", "pricing-2"), c.listed());
            assertEquals(Map.of("pricing-1", 3, "pricing-2", 3), c.send(6));

            c.crash("pricing-2");
            assertEquals(List.of("pricing-1", "pricing-2"), c.listed());
            assertEquals(Map.of("failed", 3, "pricing-1", 3), c.send(6));
            assertTrue(c.awaitListed(1));
            assertEquals(Map.of("pricing-1", 6), c.send(6));
        }
    }

    @Test
    void whenConsulIsGoneTheClientCannotAsk() throws Exception {
        try (Cluster c = three()) {
            c.consul.close();
            assertThrows(RuntimeException.class, c::listed);
        }
    }
}
