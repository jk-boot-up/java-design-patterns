package com.jk.explore.apicomposition;

/**
 * Shipping. The slowest of the three, because it asks a courier's own API.
 *
 * Being the slowest makes it the service that decides how long the page takes, however
 * the composition is written. Parallel calls cost the maximum, and this is the maximum.
 * The second constructor exists so that a demo and a test can make it slower still and
 * watch the whole page slow down with it.
 */
public final class ShippingService {

    public static final long LATENCY_MILLIS = 120;

    private final RemoteCall<String, DeliveryStatus> statusFor;
    private final long latencyMillis;

    public ShippingService(SimulatedClock clock, CallLog log) {
        this(clock, log, LATENCY_MILLIS);
    }

    public ShippingService(SimulatedClock clock, CallLog log, long latencyMillis) {
        this.latencyMillis = latencyMillis;
        this.statusFor = new RemoteCall<>("Shipping", latencyMillis,
                orderId -> new DeliveryStatus("Royal Mail", "out for delivery",
                        "today before 18:00"), clock, log);
    }

    public DeliveryStatus statusFor(String orderId) {
        return statusFor.invoke(orderId);
    }

    /** Scripts the next {@code count} calls to fail. */
    public void goDown(int count) {
        statusFor.failNext(count);
    }

    public int callsReceived() {
        return statusFor.invocations();
    }

    public long latencyMillis() {
        return latencyMillis;
    }
}
