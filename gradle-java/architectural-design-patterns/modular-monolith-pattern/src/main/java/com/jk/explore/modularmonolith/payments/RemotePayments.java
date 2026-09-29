package com.jk.explore.modularmonolith.payments;

/**
 * Payments after it has been moved into its own service: the same front door, now over the network.
 *
 * <p>Here the "network" is counted rather than real. The point is that the
 * orders module does not change at all when this replaces the in-process module.
 */
public final class RemotePayments implements PaymentsApi {

    private final PaymentsApi server = PaymentsApi.create();
    private int networkCalls;

    @Override
    public String charge(String orderId, long pence) {
        networkCalls++;
        return server.charge(orderId, pence);
    }

    @Override
    public long takenFor(String orderId) {
        networkCalls++;
        return server.takenFor(orderId);
    }

    public int networkCalls() {
        return networkCalls;
    }
}
