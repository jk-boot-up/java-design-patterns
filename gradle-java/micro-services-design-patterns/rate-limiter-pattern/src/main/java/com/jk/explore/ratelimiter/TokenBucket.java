package com.jk.explore.ratelimiter;

/**
 * A bucket that holds up to {@code capacity} tokens and gains {@code refillPerSecond} of them every second.
 * A request takes one token, or is refused. A full bucket allows a burst of {@code capacity} at once, and
 * after that the steady rate is the refill rate.
 *
 * <p>Tokens are counted in thousandths so that a partial second still refills exactly, with no floating point.
 */
public class TokenBucket {

    private final long capacityMilli;
    private final long refillPerSecond;
    private final Clock clock;
    private long milliTokens;
    private long lastRefill;

    public TokenBucket(int capacity, int refillPerSecond, Clock clock) {
        this.capacityMilli = capacity * 1000L;
        this.refillPerSecond = refillPerSecond;
        this.clock = clock;
        this.milliTokens = capacityMilli;
        this.lastRefill = clock.now();
    }

    private void refill() {
        long elapsed = clock.now() - lastRefill;
        milliTokens = Math.min(capacityMilli, milliTokens + elapsed * refillPerSecond);
        lastRefill = clock.now();
    }

    public synchronized boolean tryAcquire() {
        refill();
        if (milliTokens >= 1000) {
            milliTokens -= 1000;
            return true;
        }
        return false;
    }

    /** How long until one token is available again, in milliseconds. Zero if one is available now. */
    public synchronized long retryAfterMillis() {
        refill();
        if (milliTokens >= 1000) {
            return 0;
        }
        long missing = 1000 - milliTokens;
        return (missing + refillPerSecond - 1) / refillPerSecond;
    }
}
