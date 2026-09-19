package com.jk.explore.ratelimiter;

public class RateLimiterDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static int burst(TokenBucket bucket, int requests) {
        int allowed = 0;
        for (int i = 0; i < requests; i++) {
            if (bucket.tryAcquire()) {
                allowed++;
            }
        }
        return allowed;
    }

    private static void one() {
        System.out.println("ONE. No limit.");
        SearchService search = new SearchService(100);
        for (int i = 0; i < 1000; i++) {
            search.handle();
        }
        System.out.println("  the product search can serve " + search.capacityPerSecond() + " requests a second. a client sends 1000 in one second.");
        System.out.println("  accepted: " + search.accepted() + ". beyond what it can serve: " + search.overCapacity() + ", and every other customer waits behind them.");
    }

    private static void two() {
        System.out.println("TWO. A bucket of tokens.");
        Clock clock = new Clock();
        TokenBucket bucket = new TokenBucket(10, 5, clock);
        System.out.println("  a bucket of 10 tokens, refilled at 5 a second. a burst of 20 at once: " + burst(bucket, 20) + " allowed, " + (20 - 10) + " refused.");
        clock.advance(1000);
        System.out.println("  one second later, another 20: " + burst(bucket, 20) + " allowed.");
        clock.advance(10_000);
        System.out.println("  after ten quiet seconds the bucket is full again, and no more than full: " + burst(bucket, 20) + " allowed.");
    }

    private static void three() {
        System.out.println("THREE. A steady rate always gets through.");
        Clock clock = new Clock();
        TokenBucket bucket = new TokenBucket(10, 5, clock);
        int allowed = 0;
        for (int second = 0; second < 60; second++) {
            for (int i = 0; i < 5; i++) {
                if (bucket.tryAcquire()) {
                    allowed++;
                }
                clock.advance(200);
            }
        }
        System.out.println("  5 requests a second for a minute, evenly spaced: " + allowed + " of 300 allowed.");
        System.out.println("  a burst is tolerated up to the size of the bucket. a sustained rate above the refill is not.");
    }

    private static void four() {
        System.out.println("FOUR. One bucket for everyone, or one each.");
        Clock clock = new Clock();
        TokenBucket shared = new TokenBucket(10, 5, clock);
        int greedy = burst(shared, 10);
        System.out.println("  one shared bucket: the greedy client takes " + greedy + ". the polite client's one request: " + (shared.tryAcquire() ? "allowed" : "refused") + ".");
        RateLimiter perCaller = new RateLimiter(10, 5, clock);
        int greedyOwn = 0;
        for (int i = 0; i < 20; i++) {
            if (perCaller.tryAcquire("greedy")) {
                greedyOwn++;
            }
        }
        System.out.println("  a bucket each: the greedy client gets " + greedyOwn + " of 20. the polite client's one request: " + (perCaller.tryAcquire("polite") ? "allowed" : "refused") + ".");
    }

    private static void five() {
        System.out.println("FIVE. Say when to come back.");
        Clock clock = new Clock();
        TokenBucket bucket = new TokenBucket(2, 1, clock);
        burst(bucket, 2);
        long wait = bucket.retryAfterMillis();
        System.out.println("  the bucket is empty. the refusal says: retry after " + wait + " milliseconds.");
        clock.advance(wait - 1);
        System.out.println("  one millisecond early: " + (bucket.tryAcquire() ? "allowed" : "refused") + ".");
        clock.advance(1);
        System.out.println("  at the moment it said: " + (bucket.tryAcquire() ? "allowed" : "refused") + ".");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Clock clock = new Clock();
        int allowed = 0;
        for (int instance = 0; instance < 3; instance++) {
            allowed += burst(new TokenBucket(10, 5, clock), 30);
        }
        System.out.println("  three servers, each with its own bucket of 10: a burst of 90 is allowed " + allowed + " times, not 10. the limit is three times looser than it says.");
        RateLimiter limiter = new RateLimiter(10, 5, clock);
        for (int i = 0; i < 10_000; i++) {
            limiter.tryAcquire("client-" + i);
        }
        System.out.println("  10000 different callers: " + limiter.callersRemembered() + " buckets to keep in memory.");
        TokenBucket page = new TokenBucket(10, 5, clock);
        System.out.println("  and a real page that loads 12 things at once gets " + burst(page, 12) + " of them. the limit cannot tell a person from a script.");
    }
}
