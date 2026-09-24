package com.jk.explore.leaderelectionk8s;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.util.List;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * Asks a real API server directly. One kind cluster is made for the whole class and deleted
 * at the end of it. Every wait is a poll on the lease or on what a copy has said.
 */
class RealLeaseTest {

    private static Cluster cluster;
    private final List<ServiceCopy> copies = new java.util.ArrayList<>();

    @BeforeAll
    static void makeTheCluster() {
        assumeTrue(Cluster.containerRuntimeAvailable() && Cluster.kindAvailable(), "needs a container runtime and kind");
        cluster = new Cluster();
        cluster.create();
    }

    @AfterAll
    static void deleteTheCluster() {
        if (cluster != null) {
            cluster.close();
        }
    }

    @BeforeEach
    void startFromNoLease() {
        LeaseView.delete(cluster.client(), KubernetesLeaderElectionDemo.LEASE);
    }

    @AfterEach
    void stopTheCopies() {
        copies.forEach(ServiceCopy::close);
    }

    private ServiceCopy start(String name, Inbox inbox) {
        ServiceCopy copy = ServiceCopy.start(name, cluster.kubeconfig(), KubernetesLeaderElectionDemo.LEASE, true, inbox);
        copies.add(copy);
        copy.awaitSaying("READY");
        return copy;
    }

    @Test
    void theFirstCopyIsWrittenIntoTheLeaseAndTheOthersAreToldSo() {
        Inbox inbox = new Inbox(false);
        start("A", inbox).awaitSaying("LEADING 0");
        start("B", inbox).awaitSaying("NEW_LEADER A");
        LeaseView lease = LeaseView.read(cluster.client(), KubernetesLeaderElectionDemo.LEASE).orElseThrow();
        assertEquals("A", lease.holder());
        assertEquals(0, lease.transitions());
        assertEquals(5, lease.durationSeconds());
    }

    @Test
    void theApiServerRefusesASecondWriteBasedOnTheSameVersion() {
        start("A", new Inbox(false)).awaitSaying("LEADING 0");
        copies.forEach(ServiceCopy::close);
        assertEquals("refused with 409 Conflict", KubernetesLeaderElectionDemo.twoWritesFromOneVersion(cluster.client()));
        assertEquals("B", LeaseView.holder(cluster.client(), KubernetesLeaderElectionDemo.LEASE));
    }

    @Test
    void aFrozenLeaderLosesTheLeaseAndIsOnlyToldWhenItWakes() {
        Inbox inbox = new Inbox(true);
        ServiceCopy a = start("A", inbox);
        a.awaitSaying("LEADING 0");
        ServiceCopy b = start("B", inbox);
        b.awaitSaying("NEW_LEADER A");
        a.freeze();
        b.awaitSaying("LEADING 1");
        assertEquals("B", LeaseView.holder(cluster.client(), KubernetesLeaderElectionDemo.LEASE));
        assertTrue(!a.said("STOPPED"), "a frozen process cannot be told anything");
        a.wake();
        a.awaitSaying("STOPPED");
    }

    @Test
    void aCleanShutdownHandsTheLeaseOverWithinOneLease() {
        Inbox inbox = new Inbox(false);
        ServiceCopy a = start("A", inbox);
        a.awaitSaying("LEADING 0");
        ServiceCopy b = start("B", inbox);
        b.awaitSaying("NEW_LEADER A");
        long started = System.nanoTime();
        a.stopCleanly();
        b.awaitSaying("LEADING 1");
        long seconds = (System.nanoTime() - started) / 1_000_000_000L;
        assertTrue(seconds < 5, "handover took " + seconds + " seconds");
    }
}
