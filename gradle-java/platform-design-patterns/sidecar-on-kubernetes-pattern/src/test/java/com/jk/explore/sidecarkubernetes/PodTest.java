package com.jk.explore.sidecarkubernetes;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PodTest {

    private static final ContainerSpec CHECKOUT = new ContainerSpec("checkout", "shop/checkout:1", 8080);

    private Pod podWithSidecar(Cluster cluster) {
        return cluster.schedule(PodSpec.of("checkout", CHECKOUT).withContainer(Injector.PROXY));
    }

    @Test
    void composeSharesANetworkOnlyWhenTheFileSaysSo() {
        Compose shared = new Compose();
        shared.up(CHECKOUT, null);
        shared.up(Injector.PROXY, "checkout");
        assertTrue(shared.localhostReaches("checkout", 8081));

        Compose forgotten = new Compose();
        forgotten.up(CHECKOUT, null);
        forgotten.up(Injector.PROXY, null);
        assertFalse(forgotten.localhostReaches("checkout", 8081));
    }

    @Test
    void aPodSharesItsNetworkByDefinitionWithNothingToForget() {
        Pod pod = podWithSidecar(new Cluster());
        assertTrue(pod.network().reachable(8081));
        assertTrue(pod.network().reachable(8080));
    }

    @Test
    void twoPodsDoNotShareANetwork() {
        Cluster cluster = new Cluster();
        Pod a = podWithSidecar(cluster);
        Pod b = cluster.schedule(PodSpec.of("refunds", new ContainerSpec("refunds", "shop/refunds:1", 8080)));
        assertNotEquals(a.network().address(), b.network().address());
        assertFalse(b.network().reachable(8081), "the proxy is in the other Pod");
    }

    @Test
    void stoppingOneComposeContainerLeavesTheOtherRunning() {
        Compose compose = new Compose();
        compose.up(CHECKOUT, null);
        compose.up(Injector.PROXY, "checkout");
        compose.stop("checkout");
        assertTrue(compose.running("sidecar-proxy"));
    }

    @Test
    void deletingAPodDeletesEveryContainerAndItsReplacementIsNewOnANewAddress() {
        Cluster cluster = new Cluster();
        Pod first = podWithSidecar(cluster);
        String address = first.network().address();
        cluster.delete(first);
        assertFalse(first.container("checkout").running());
        assertFalse(first.container("sidecar-proxy").running());
        Pod second = cluster.schedule(first.spec());
        assertNotEquals(address, second.network().address());
        assertEquals(0, second.container("checkout").restarts());
    }

    @Test
    void aCrashedContainerIsRestartedAloneAndItsNeighbourIsUntouched() {
        Cluster cluster = new Cluster();
        Pod pod = podWithSidecar(cluster);
        cluster.crash(pod, "sidecar-proxy");
        assertEquals("1/2", pod.ready());
        assertTrue(pod.container("checkout").running(), "a crash does not take a neighbour with it");
        assertEquals("connection refused on localhost:8081", ServiceCall.pay(pod));
        cluster.kubeletReconciles(pod);
        assertEquals("2/2", pod.ready());
        assertEquals(1, pod.container("sidecar-proxy").restarts());
        assertEquals(0, pod.container("checkout").restarts());
        assertEquals("paid, through the proxy", ServiceCall.pay(pod));
    }

    @Test
    void aPodIsReadyForTrafficOnlyWhenEveryContainerIs() {
        Cluster cluster = new Cluster();
        Pod pod = podWithSidecar(cluster);
        assertTrue(pod.isReady());
        cluster.crash(pod, "sidecar-proxy");
        assertFalse(pod.isReady());
    }

    @Test
    void injectionAddsASidecarWithoutChangingTheAuthoredManifest() {
        PodSpec authored = PodSpec.of("refunds", new ContainerSpec("refunds", "shop/refunds:1", 8080));
        PodSpec copy = PodSpec.of("refunds", new ContainerSpec("refunds", "shop/refunds:1", 8080));
        PodSpec created = Injector.inject(authored);
        assertEquals(copy, authored, "the authored manifest is untouched");
        assertEquals(List.of("refunds", "sidecar-proxy"), created.containers().stream().map(ContainerSpec::name).toList());
        assertEquals(created, Injector.inject(created), "injecting twice adds nothing");
    }

    @Test
    void containersStartedTogetherLeaveARaceAndANativeSidecarStartsFirst() {
        Cluster cluster = new Cluster();
        PodSpec spec = PodSpec.of("checkout", CHECKOUT).withContainer(Injector.PROXY);
        assertEquals(List.of("checkout", "sidecar-proxy"), cluster.schedule(spec).startOrder());
        assertEquals(List.of("sidecar-proxy", "checkout"), cluster.schedule(spec.withSidecarsFirst(true)).startOrder());
    }
}
