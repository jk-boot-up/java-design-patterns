package com.jk.explore.sidecarkubernetes;

/** The checkout service making a payment: one call, to {@code localhost:8081}, which it hopes is a proxy. */
public final class ServiceCall {

    public static final int PROXY_PORT = 8081;

    private ServiceCall() {
    }

    public static String pay(Pod pod) {
        if (!pod.container("checkout").running()) {
            return "checkout is not running";
        }
        return pod.network().reachable(PROXY_PORT) ? "paid, through the proxy" : "connection refused on localhost:" + PROXY_PORT;
    }
}
