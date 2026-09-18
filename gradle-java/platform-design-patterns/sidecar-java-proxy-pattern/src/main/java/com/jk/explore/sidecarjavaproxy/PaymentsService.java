package com.jk.explore.sidecarjavaproxy;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * Checkout, exactly as §41 left it, and the point is that this file is boring.
 *
 * <p>Read every line of it. There is a name, an address, and a method that hands a
 * payment to the address. There is no retry loop, no backoff, no deadline, no keystore,
 * no counter and no mention of the payment provider. That emptiness was §41's
 * achievement; this project inherits it and does not add to it.
 *
 * <p>What this project adds is a way to prove the service is untouched.
 * {@link #startNumber} is the running count of how many times a
 * {@code PaymentsService} has been constructed since the program began — a stand-in for
 * the container's start time, which is what the deployed demo reads out of Docker. The
 * demo creates exactly one of these, in {@code main}, and every act is handed that same
 * instance. So when the proxy is swapped and this number has not moved, the reason is
 * not that the demo was careful. It is that there is only one {@code new
 * PaymentsService(...)} in the whole program, and a swap is not a place where one could
 * go.
 */
public final class PaymentsService {

    /** Bumped by every construction, so the demo can show that none happened. */
    private static final AtomicInteger STARTS = new AtomicInteger();

    public static final String NAME = "checkout";

    private final String name;
    private final LocalPort port;
    private final int startNumber;

    public PaymentsService(String name, LocalPort port) {
        this.name = name;
        this.port = port;
        this.startNumber = STARTS.incrementAndGet();
    }

    public String name() {
        return name;
    }

    /** Which start of this service this instance is. A restart would make it larger. */
    public int startNumber() {
        return startNumber;
    }

    /** How many times any payments service has started in this program. */
    public static int startsSoFar() {
        return STARTS.get();
    }

    /**
     * Puts the count back to nothing, because a program begins with nothing running.
     *
     * <p>{@code main} calls this on its first line. It matters only under test: the test
     * suite runs every class in one JVM, so without it the count the demo prints would
     * depend on which tests happened to run first, and a figure that moves for reasons
     * unrelated to the lesson is a figure no document can quote.
     */
    public static void nothingIsRunningYet() {
        STARTS.set(0);
    }

    /**
     * The one line of configuration the service has about how it reaches the provider,
     * which is not about the provider at all.
     */
    public String configuredEndpoint() {
        return "http://" + port.address() + "/pay";
    }

    public LocalPort port() {
        return port;
    }

    /** Takes the money. Or rather, asks the neighbour to. */
    public Receipt pay(Payment payment) {
        return port.send(payment);
    }
}
