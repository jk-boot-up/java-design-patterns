package com.jk.explore.sidecarkubernetes;

/** Six acts. Tier 1: a plain-Java model of what a Pod guarantees. Nothing here starts a container. */
public final class PodDemo {

    static final ContainerSpec CHECKOUT = new ContainerSpec("checkout", "shop/checkout:1", 8080);

    public static void main(String[] args) {
        System.out.println("SIDECAR ON KUBERNETES — two containers, one Pod\n");
        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. Shared by configuration, or shared by definition.");
        Compose compose = new Compose();
        compose.up(CHECKOUT, null);
        compose.up(Injector.PROXY, "checkout");
        System.out.println("  Compose, with network_mode: service:checkout: checkout reaches localhost:8081: "
                + compose.localhostReaches("checkout", 8081));
        Compose forgot = new Compose();
        forgot.up(CHECKOUT, null);
        forgot.up(Injector.PROXY, null);
        System.out.println("  Compose, with that one line forgotten:        checkout reaches localhost:8081: "
                + forgot.localhostReaches("checkout", 8081));
        Pod pod = new Cluster().schedule(PodSpec.of("checkout", CHECKOUT).withContainer(Injector.PROXY));
        System.out.println("  a Pod: checkout reaches localhost:8081: " + pod.network().reachable(8081)
                + ". there is no line to forget.");
        System.out.println("  both containers are on " + pod.network().address() + ", one network, because that is what a Pod is.\n");
    }

    private static void actTwo() {
        System.out.println("TWO. One lifecycle.");
        Compose compose = new Compose();
        compose.up(CHECKOUT, null);
        compose.up(Injector.PROXY, "checkout");
        compose.stop("checkout");
        System.out.println("  Compose: checkout stopped. the proxy is still running: " + compose.running("sidecar-proxy") + ".");
        Cluster cluster = new Cluster();
        Pod first = cluster.schedule(PodSpec.of("checkout", CHECKOUT).withContainer(Injector.PROXY));
        String before = first.network().address();
        cluster.delete(first);
        System.out.println("  Pod: deleted. checkout running: " + first.container("checkout").running()
                + ", proxy running: " + first.container("sidecar-proxy").running() + ". they go together.");
        Pod second = cluster.schedule(first.spec());
        System.out.println("  the replacement is a new Pod on a new address (" + before + " became " + second.network().address()
                + "), with both containers new.\n");
    }

    private static void actThree() {
        System.out.println("THREE. Restarts, however, are per container.");
        Cluster cluster = new Cluster();
        Pod pod = cluster.schedule(PodSpec.of("checkout", CHECKOUT).withContainer(Injector.PROXY));
        cluster.crash(pod, "sidecar-proxy");
        System.out.println("  the proxy's process dies. the Pod is " + pod.ready() + ". a payment now: " + ServiceCall.pay(pod));
        cluster.kubeletReconciles(pod);
        System.out.println("  the kubelet restarts the proxy alone. Pod " + pod.ready() + ", proxy restarts "
                + pod.container("sidecar-proxy").restarts() + ", checkout restarts " + pod.container("checkout").restarts() + ".");
        System.out.println("  a payment now: " + ServiceCall.pay(pod));
        System.out.println("  the service was not touched, and its calls failed for the gap. a crash does not take a neighbour with it.");
        System.out.println("  what is shared is the Pod: scheduling, eviction and deletion, not process death.\n");
    }

    private static void actFour() {
        System.out.println("FOUR. Injection.");
        PodSpec authored = PodSpec.of("refunds", new ContainerSpec("refunds", "shop/refunds:1", 8080));
        PodSpec created = Injector.inject(authored);
        System.out.println("  the manifest the refunds team wrote lists " + authored.containers().size() + " container: "
                + authored.containers().stream().map(ContainerSpec::name).toList());
        System.out.println("  the Pod that was created lists " + created.containers().size() + ": "
                + created.containers().stream().map(ContainerSpec::name).toList());
        System.out.println("  the authored manifest is unchanged: " + (authored.containers().size() == 1)
                + ". the sidecar arrived from outside.");
        System.out.println("  that is the mechanism a service mesh is built on: every Pod gets a proxy, and no team wrote it.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. READY 2/2, and the start-up race.");
        Cluster cluster = new Cluster();
        Pod healthy = cluster.schedule(PodSpec.of("checkout", CHECKOUT).withContainer(Injector.PROXY));
        System.out.println("  kubectl get pods: checkout   READY " + healthy.ready() + "   one logical service, two containers.");
        cluster.crash(healthy, "sidecar-proxy");
        System.out.println("  with the proxy down it reads " + healthy.ready() + ", and the Pod is ready for traffic: " + healthy.isReady() + ".");
        PodSpec parallel = PodSpec.of("checkout", CHECKOUT).withContainer(Injector.PROXY);
        Pod racing = cluster.schedule(parallel);
        System.out.println("  containers started together, in manifest order: " + racing.startOrder()
                + ". the service can start, and call the proxy, before the proxy is listening.");
        Pod ordered = cluster.schedule(parallel.withSidecarsFirst(true));
        System.out.println("  a native sidecar starts first: " + ordered.startOrder() + ". the ordering problem is gone.\n");
    }

    private static void actSix() {
        System.out.println("SIX. The bill, and the honest question.");
        System.out.println("  everything the Compose version cost, plus a cluster: a scheduler, a control plane,");
        System.out.println("  a YAML dialect and a networking model, added to a shop that worked with two containers and a file.");
        System.out.println("  do you need Kubernetes yet? for four services: almost certainly not. for a fleet: this is the bargain.");
        System.out.println("  what this model does not show: a real scheduler, real restarts with back-off, a control plane that fails.");
        System.out.println("  where you have met this: every Pod in every cluster, and every service mesh's injected proxy.");
    }
}
