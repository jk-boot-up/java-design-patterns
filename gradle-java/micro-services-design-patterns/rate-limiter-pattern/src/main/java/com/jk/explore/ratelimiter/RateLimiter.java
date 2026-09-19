package com.jk.explore.ratelimiter;

import java.util.HashMap;
import java.util.Map;

/** One bucket per caller, so one caller's burst cannot use up another's allowance. */
public class RateLimiter {

    private final int capacity;
    private final int refillPerSecond;
    private final Clock clock;
    private final Map<String, TokenBucket> buckets = new HashMap<>();

    public RateLimiter(int capacity, int refillPerSecond, Clock clock) {
        this.capacity = capacity;
        this.refillPerSecond = refillPerSecond;
        this.clock = clock;
    }

    public synchronized TokenBucket bucketFor(String caller) {
        return buckets.computeIfAbsent(caller, c -> new TokenBucket(capacity, refillPerSecond, clock));
    }

    public boolean tryAcquire(String caller) {
        return bucketFor(caller).tryAcquire();
    }

    public synchronized int callersRemembered() {
        return buckets.size();
    }
}
