package com.jk.explore.servicemesh;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class ServiceMeshTest {

    @Test
    void libraryClientsBehaveDifferently() {
        assertTrue(new LibraryClient("a", 3).call(new Flaky(2)));
        assertFalse(new LibraryClient("b", 0).call(new Flaky(2)));
        assertFalse(new LibraryClient("c", 1).call(new Flaky(2)));
    }

    @Test
    void oneMeshPolicyRetriesForEveryone() {
        Mesh mesh = new Mesh();
        mesh.register("payments", new Flaky(2));
        mesh.setRetries(3);
        assertTrue(mesh.call("checkout", "payments"));
    }

    @Test
    void changingThePolicyChangesTheResult() {
        Mesh mesh = new Mesh();
        mesh.register("payments", new Flaky(2));
        mesh.setRetries(0);
        assertFalse(mesh.call("checkout", "payments"));
    }

    @Test
    void unknownCallersAreTurnedAwayBeforeTheService() {
        Mesh mesh = new Mesh();
        Flaky payments = new Flaky(0);
        mesh.register("payments", payments);
        mesh.allowOnly("payments", Set.of("checkout"));
        assertTrue(mesh.call("checkout", "payments"));
        assertFalse(mesh.call("gift-cards", "payments"));
        assertEquals(1, payments.received());
        assertEquals(1, mesh.denied());
    }

    @Test
    void metricsAreKeptByThePairAndRetriesMultiplyLoad() {
        Mesh mesh = new Mesh();
        Flaky payments = new Flaky(2);
        mesh.register("payments", payments);
        mesh.setRetries(3);
        mesh.call("checkout", "payments");
        assertEquals(List.of("checkout->payments calls 1, failed 0, attempts 3"), mesh.report());
        assertEquals(3, payments.received());
        assertEquals(3 * Mesh.TICKS_THROUGH_PROXIES, mesh.ticks());
    }
}
