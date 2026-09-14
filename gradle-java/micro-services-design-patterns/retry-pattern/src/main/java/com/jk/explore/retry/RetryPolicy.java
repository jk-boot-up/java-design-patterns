package com.jk.explore.retry;

import java.util.Random;

/**
 * How many times to try, and how long to wait between attempts.
 *
 * "Backoff" means the waits get longer: a hundred milliseconds, then two hundred,
 * then four hundred. The reason is not politeness. If a payment gateway is
 * struggling because it is overloaded, a thousand callers retrying immediately are
 * the overload — backing off gives it room to recover, which is the only thing that
 * will make the next attempt succeed.
 *
 * <p>"Jitter" means each caller waits a slightly different amount. Without it, a
 * thousand callers who all failed at the same moment all retry at the same moment,
 * and the stampede simply repeats on a delay. The jitter here is drawn from a
 * seeded {@link Random} so that the demo and the tests get the same numbers every
 * run; in production the seed comes from the machine.
 */
public final class RetryPolicy {

    private final int maxAttempts;
    private final long initialDelayMillis;
    private final int multiplier;
    private final int jitterPercent;
    private final Random random;

    public RetryPolicy(int maxAttempts, long initialDelayMillis, int multiplier,
                       int jitterPercent, long seed) {
        if (maxAttempts < 1) {
            throw new IllegalArgumentException("a policy that never tries is not a policy");
        }
        this.maxAttempts = maxAttempts;
        this.initialDelayMillis = initialDelayMillis;
        this.multiplier = multiplier;
        this.jitterPercent = jitterPercent;
        this.random = new Random(seed);
    }

    /** Three attempts, 100ms doubling, with a little jitter. The usual starting point. */
    public static RetryPolicy threeAttempts(long seed) {
        return new RetryPolicy(3, 100, 2, 20, seed);
    }

    /** Three attempts and no waiting at all, for showing what jitter is worth. */
    public static RetryPolicy threeAttemptsNoBackoff() {
        return new RetryPolicy(3, 0, 1, 0, 0L);
    }

    public int maxAttempts() {
        return maxAttempts;
    }

    /**
     * How long to wait before attempt number {@code attempt}.
     *
     * @param attempt 1 for the first attempt, which never waits
     */
    public long delayBeforeAttempt(int attempt) {
        if (attempt <= 1) {
            return 0;
        }
        long base = initialDelayMillis;
        for (int i = 2; i < attempt; i++) {
            base *= multiplier;
        }
        return base + jitterFor(base);
    }

    private long jitterFor(long base) {
        if (jitterPercent == 0 || base == 0) {
            return 0;
        }
        long spread = (base * jitterPercent) / 100;
        return random.nextLong(spread + 1);
    }

    /** The waits without their jitter, which is what the documentation can promise. */
    public long baseDelayBeforeAttempt(int attempt) {
        if (attempt <= 1) {
            return 0;
        }
        long base = initialDelayMillis;
        for (int i = 2; i < attempt; i++) {
            base *= multiplier;
        }
        return base;
    }
}
