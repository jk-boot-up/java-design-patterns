package com.jk.explore.servicediscovery;

import java.util.function.Function;

/**
 * One remote endpoint, simulated.
 *
 * There is no network in this project. A remote call is this class: it advances
 * the clock by however long the link takes, writes a line into the call log,
 * and then either returns the answer or throws. Whether the thing underneath is
 * an HTTP request or a plain method call makes no difference to any of the
 * patterns in this category, which is exactly why they can be taught this way.
 *
 * <p>Two knobs make the failures in the demo reproducible. The latency is fixed
 * per link, so a call over the mobile network is genuinely twenty times slower
 * than a call between two services in the same data centre. And
 * {@link #failNext(int)} scripts the next few invocations to fail, so a test
 * asserts what the pattern did rather than what chance did.
 *
 * @param <A> the argument the endpoint takes, such as a product code
 * @param <T> what it answers with
 */
public final class RemoteCall<A, T> {

    private final String serviceName;
    private final long latencyMillis;
    private final Function<A, T> work;
    private final SimulatedClock clock;
    private final CallLog log;

    private int failuresRemaining;
    private int invocations;

    public RemoteCall(String serviceName, long latencyMillis, Function<A, T> work,
                      SimulatedClock clock, CallLog log) {
        this.serviceName = serviceName;
        this.latencyMillis = latencyMillis;
        this.work = work;
        this.clock = clock;
        this.log = log;
    }

    /**
     * Scripts the next {@code count} invocations to fail, then behave normally.
     * "Fail twice, then succeed" is one call to this method.
     */
    public RemoteCall<A, T> failNext(int count) {
        this.failuresRemaining = count;
        return this;
    }

    /**
     * Makes the call. Time passes on the clock whether it succeeds or not.
     *
     * <p>The latency is spent in two halves, one on the way out and one on the
     * way back, with the service's own work in between. That matters for one
     * reason only: a call can contain other calls. A caller's single call to one
     * service takes a slow trip out, and anything that service does to other
     * services happens <em>inside</em> that trip. Charging the whole latency up
     * front would put the inner calls after the outer call had already finished,
     * and the timeline would be a lie.
     */
    public T invoke(A argument) {
        invocations++;
        long startedAt = clock.millis();
        clock.advance(latencyMillis / 2);

        if (failuresRemaining > 0) {
            failuresRemaining--;
            clock.advance(latencyMillis - latencyMillis / 2);
            log.record(startedAt, clock.millis(), serviceName, "FAILED", "no answer");
            throw new ServiceUnavailableException(serviceName);
        }

        T answer = work.apply(argument);
        clock.advance(latencyMillis - latencyMillis / 2);
        log.record(startedAt, clock.millis(), serviceName, "OK", describe(answer));
        return answer;
    }

    /** How many times this endpoint has been called, successfully or not. */
    public int invocations() {
        return invocations;
    }

    public String serviceName() {
        return serviceName;
    }

    /** How long one call over this link takes, in simulated milliseconds. */
    public long latencyMillis() {
        return latencyMillis;
    }

    private static String describe(Object answer) {
        String text = String.valueOf(answer);
        return text.length() <= 44 ? text : text.substring(0, 41) + "...";
    }
}
