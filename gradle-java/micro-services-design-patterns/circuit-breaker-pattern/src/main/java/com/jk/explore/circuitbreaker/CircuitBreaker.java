package com.jk.explore.circuitbreaker;

import java.util.function.Supplier;

/**
 * Counts failures, and once there have been enough in a row, stops calling.
 *
 * The rule is short enough to say in one breath. While the breaker is closed, every
 * call goes through and consecutive failures are counted; when the count reaches the
 * threshold the breaker opens. While it is open, no call is made at all — the caller
 * is refused instantly. After the reset wait has passed, one single call is allowed
 * through: if it works the breaker closes and the count goes back to zero, and if it
 * fails the breaker opens again for another full wait.
 *
 * <p>Note the word <em>consecutive</em>. One success resets the count, because a
 * service that answers three times and fails once is not down; it is a service with
 * a bad moment, and the retry pattern already handles that.
 *
 * <p>This class holds no fallback and knows nothing about what the caller will do
 * when refused. That is deliberate: the right answer differs per dependency, and
 * only the caller knows it.
 */
public final class CircuitBreaker {

    private final String serviceName;
    private final int failureThreshold;
    private final long resetAfterMillis;
    private final SimulatedClock clock;
    private final CallLog log;

    private BreakerState state = BreakerState.CLOSED;
    private int consecutiveFailures;
    private long openedAt;
    private int callsMade;
    private int callsRefused;

    /**
     * @param failureThreshold how many failures in a row before it opens
     * @param resetAfterMillis how long to stay open before trying one call
     */
    public CircuitBreaker(String serviceName, int failureThreshold, long resetAfterMillis,
                          SimulatedClock clock, CallLog log) {
        this.serviceName = serviceName;
        this.failureThreshold = failureThreshold;
        this.resetAfterMillis = resetAfterMillis;
        this.clock = clock;
        this.log = log;
    }

    /**
     * Makes the call, unless the breaker has decided not to.
     *
     * @throws CircuitOpenException without calling anything, if the breaker is open
     */
    public <T> T call(Supplier<T> action) {
        if (state == BreakerState.OPEN) {
            if (clock.millis() - openedAt < resetAfterMillis) {
                callsRefused++;
                log.note(serviceName, "REFUSED", "circuit open, no call made");
                throw new CircuitOpenException(serviceName);
            }
            // The wait is over. Let exactly one call through and see.
            state = BreakerState.HALF_OPEN;
            log.note(serviceName, "HALF-OPEN", "letting one call through to test");
        }

        try {
            callsMade++;
            T answer = action.get();
            onSuccess();
            return answer;
        } catch (RuntimeException failure) {
            onFailure(failure);
            throw failure;
        }
    }

    private void onSuccess() {
        if (state == BreakerState.HALF_OPEN) {
            log.note(serviceName, "CLOSED", "the probe worked, calls resume");
        }
        state = BreakerState.CLOSED;
        consecutiveFailures = 0;
    }

    private void onFailure(RuntimeException failure) {
        if (state == BreakerState.HALF_OPEN) {
            // Still broken. Straight back to open, for another full wait.
            trip("the probe failed too");
            return;
        }
        consecutiveFailures++;
        if (consecutiveFailures >= failureThreshold) {
            trip(consecutiveFailures + " failures in a row");
        } else {
            log.note(serviceName, "FAILED", "failure " + consecutiveFailures
                    + " of " + failureThreshold);
        }
    }

    private void trip(String why) {
        state = BreakerState.OPEN;
        openedAt = clock.millis();
        log.note(serviceName, "OPENED", why + ", not calling for " + resetAfterMillis + "ms");
    }

    public BreakerState state() {
        return state;
    }

    public int consecutiveFailures() {
        return consecutiveFailures;
    }

    /** How many calls actually reached the service. */
    public int callsMade() {
        return callsMade;
    }

    /** How many calls were refused without being made. Each one is a saved timeout. */
    public int callsRefused() {
        return callsRefused;
    }
}
