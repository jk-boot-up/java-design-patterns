package com.jk.explore.sidecarjavaproxy;

/**
 * The address the service sends its payments to, and the only thing the swap touches.
 *
 * <p>In the deployed version this is {@code localhost:8081}. The service has that string
 * in its configuration and nothing else: no provider hostname, no certificate, no retry
 * count. Whatever happens to be listening on the port answers, and the service has no
 * way of finding out what that is and no reason to want to.
 *
 * <p><b>This class is the pattern's hinge.</b> A sidecar is swappable because the
 * contract between a service and its proxy is an address rather than a library, a
 * language or a build. Replace what is bound to the port and the service is already
 * talking to the new thing, without being told, rebuilt, restarted or even paused. Every
 * claim this project makes reduces to that one sentence.
 *
 * <p>{@link #vacate()} exists because the swap has a cost and the cost is measured in
 * milliseconds of nothing listening. Between the old proxy stopping and the new one
 * accepting connections, the port is empty, and a payment that arrives in that window
 * does not fail over to anything — the service deleted its own retry code in §41, on
 * purpose. The demo shows that window rather than skipping over it.
 */
public final class LocalPort {

    /** The port number the service was configured with, once, at the beginning. */
    public static final int NUMBER = 8081;

    private Proxy listening;
    private int swaps;

    public LocalPort(Proxy initial) {
        this.listening = initial;
    }

    /**
     * Puts a different proxy on the port.
     *
     * <p>Notice what this method does not take: any reference to the service, anything
     * it could use to notify one, and anything it could use to restart one. There is no
     * such parameter because there is no such step.
     */
    public void install(Proxy proxy) {
        this.listening = proxy;
        this.swaps++;
    }

    /** Leaves the port with nothing on it, which is what the middle of a swap looks like. */
    public void vacate() {
        this.listening = null;
    }

    public Proxy occupant() {
        return listening;
    }

    /** How many times the thing on this port has been replaced. */
    public int swaps() {
        return swaps;
    }

    public String address() {
        return "localhost:" + NUMBER;
    }

    /** Hands the payment to whatever is listening, or fails because nothing is. */
    public Receipt send(Payment payment) {
        if (listening == null) {
            throw new PaymentFailed(PaymentFailed.Reason.NOTHING_LISTENING,
                    "connection refused to " + address() + " — nothing is listening");
        }
        return listening.forward(payment);
    }
}
