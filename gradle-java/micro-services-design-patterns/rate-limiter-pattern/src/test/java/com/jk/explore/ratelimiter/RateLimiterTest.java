package com.jk.explore.ratelimiter;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class RateLimiterTest {

    private static int burst(TokenBucket b, int n) {
        int ok = 0;
        for (int i = 0; i < n; i++) if (b.tryAcquire()) ok++;
        return ok;
    }

    @Test
    void aBurstIsLimitedToTheCapacityAndThenRefillsAtTheRate() {
        Clock c = new Clock();
        TokenBucket b = new TokenBucket(10, 5, c);
        assertEquals(10, burst(b, 20));
        c.advance(1000);
        assertEquals(5, burst(b, 20));
    }

    @Test
    void aBucketNeverHoldsMoreThanItsCapacity() {
        Clock c = new Clock();
        TokenBucket b = new TokenBucket(10, 5, c);
        burst(b, 10);
        c.advance(3_600_000);
        assertEquals(10, burst(b, 50));
    }

    @Test
    void aSteadyRateAtTheRefillRateIsNeverRefused() {
        Clock c = new Clock();
        TokenBucket b = new TokenBucket(10, 5, c);
        for (int i = 0; i < 300; i++) {
            assertTrue(b.tryAcquire(), "request " + i);
            c.advance(200);
        }
    }

    @Test
    void aSteadyRateAboveTheRefillRateIsEventuallyRefused() {
        Clock c = new Clock();
        TokenBucket b = new TokenBucket(10, 5, c);
        int refused = 0;
        for (int i = 0; i < 300; i++) {
            if (!b.tryAcquire()) refused++;
            c.advance(100);
        }
        assertTrue(refused > 100);
    }

    @Test
    void partialSecondsRefillExactly() {
        Clock c = new Clock();
        TokenBucket b = new TokenBucket(1, 4, c);
        assertTrue(b.tryAcquire());
        c.advance(249);
        assertFalse(b.tryAcquire());
        c.advance(1);
        assertTrue(b.tryAcquire());
    }

    @Test
    void retryAfterIsExact() {
        Clock c = new Clock();
        TokenBucket b = new TokenBucket(2, 1, c);
        burst(b, 2);
        long wait = b.retryAfterMillis();
        assertEquals(1000, wait);
        c.advance(wait - 1);
        assertFalse(b.tryAcquire());
        c.advance(1);
        assertTrue(b.tryAcquire());
        assertEquals(0, new TokenBucket(2, 1, c).retryAfterMillis());
    }

    @Test
    void aBucketEachKeepsAGreedyCallerFromStarvingAPoliteOne() {
        Clock c = new Clock();
        RateLimiter l = new RateLimiter(10, 5, c);
        for (int i = 0; i < 100; i++) l.tryAcquire("greedy");
        assertTrue(l.tryAcquire("polite"));
        TokenBucket shared = new TokenBucket(10, 5, c);
        burst(shared, 10);
        assertFalse(shared.tryAcquire());
    }

    @Test
    void perServerBucketsAllowTheLimitTimesTheServers() {
        int allowed = 0;
        Clock c = new Clock();
        for (int i = 0; i < 3; i++) allowed += burst(new TokenBucket(10, 5, c), 30);
        assertEquals(30, allowed);
    }

    @Test
    void everyCallerCostsABucket() {
        RateLimiter l = new RateLimiter(10, 5, new Clock());
        for (int i = 0; i < 1000; i++) l.tryAcquire("c" + i);
        assertEquals(1000, l.callersRemembered());
    }

    @Test
    void theSearchServiceCountsWhatIsBeyondItsCapacity() {
        SearchService s = new SearchService(100);
        for (int i = 0; i < 1000; i++) s.handle();
        assertEquals(900, s.overCapacity());
    }
}
