package com.jk.explore.retry;

import java.util.function.Supplier;

/**
 * The pattern: try, and if the failure looks temporary, wait and try again.
 *
 * There are only two decisions in this class and both are worth saying out loud.
 *
 * <p><strong>Is this failure worth retrying?</strong> A timeout might not happen
 * again, so it is. A declined card will happen again every time, so it is not — and
 * a retrier that cannot tell the difference turns a clear "no" into three slow
 * "no"s.
 *
 * <p><strong>How long do I wait?</strong> Longer each time, plus a small random
 * amount. Waiting is what gives a struggling service room to recover; the random
 * part is what stops a thousand callers retrying in unison.
 *
 * <p>What this class deliberately does <em>not</em> do is make the operation safe to
 * repeat. It cannot. That has to come from the caller, in the shape of an
 * idempotency key, and no amount of care in here will substitute for it.
 */
public final class Retrier {

    private final RetryPolicy policy;
    private final SimulatedClock clock;
    private final CallLog log;
    private int attemptsMade;
    private long waitedMillis;

    public Retrier(RetryPolicy policy, SimulatedClock clock, CallLog log) {
        this.policy = policy;
        this.clock = clock;
        this.log = log;
    }

    /**
     * Runs {@code action}, retrying it while the failures look temporary.
     *
     * @param what a name for the timeline
     * @param action the call to make; it must be safe to run more than once
     * @return whatever the action returned on the attempt that worked
     * @throws RuntimeException the last failure, if every attempt failed or the
     *         failure was permanent
     */
    public <T> T call(String what, Supplier<T> action) {
        RuntimeException lastFailure = null;

        for (int attempt = 1; attempt <= policy.maxAttempts(); attempt++) {
            long delay = policy.delayBeforeAttempt(attempt);
            if (delay > 0) {
                clock.advance(delay);
                waitedMillis += delay;
                log.note("Retrier", "WAITED", delay + "ms before attempt " + attempt);
            }

            attemptsMade++;
            try {
                T answer = action.get();
                if (attempt > 1) {
                    log.note("Retrier", "RECOVERED", what + " succeeded on attempt " + attempt);
                }
                return answer;
            } catch (RuntimeException failure) {
                lastFailure = failure;
                if (!worthRetrying(failure)) {
                    log.note("Retrier", "PERMANENT", "not retrying: " + failure.getMessage());
                    throw failure;
                }
                log.note("Retrier", "RETRYABLE", "attempt " + attempt + " failed: "
                        + failure.getMessage());
            }
        }

        log.note("Retrier", "GAVE-UP", what + " failed " + policy.maxAttempts() + " times");
        throw lastFailure;
    }

    /**
     * Which failures are worth another go.
     *
     * A timeout is; a declined card is not. Everything else is treated as permanent,
     * because "retry unless I recognise it" is the rule that eventually retries a
     * bug in your own code four hundred times.
     */
    private boolean worthRetrying(RuntimeException failure) {
        return failure instanceof GatewayTimeoutException;
    }

    /** How many times the action was actually run. */
    public int attemptsMade() {
        return attemptsMade;
    }

    /** How long was spent waiting between attempts. */
    public long waitedMillis() {
        return waitedMillis;
    }
}
