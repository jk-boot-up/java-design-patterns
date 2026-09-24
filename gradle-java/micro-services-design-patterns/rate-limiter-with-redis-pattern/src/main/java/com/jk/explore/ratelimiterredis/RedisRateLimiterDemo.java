package com.jk.explore.ratelimiterredis;

import io.github.bucket4j.ConsumptionProbe;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

/**
 * Six acts against a real Redis server, started and stopped by this program.
 *
 * <p>The shop's product search runs as several copies behind a load balancer. The first act
 * gives each copy its own bucket and shows the limit leak. The rest move the bucket into
 * Redis with Bucket4j and show what holds, what the tool does to keep it holding, and what
 * it costs.
 */
public class RedisRateLimiterDemo {

    private static final String GREEDY = "client-42";

    public static void main(String[] args) {
        if (!Redis.containerRuntimeAvailable()) {
            System.out.println(Redis.NO_RUNTIME_ADVICE);
            return;
        }
        try (Redis redis = new Redis()) {
            try {
                redis.start();
            } catch (RuntimeException e) {
                System.out.println(Redis.WOULD_NOT_START_ADVICE);
                return;
            }
            one();
            two(redis);
            three(redis);
            four(redis);
            five(redis);
            six(redis);
        }
    }

    /** Each server keeps its own buckets in memory. The limit multiplies by the server count. */
    private static void one() {
        System.out.println("ONE. A bucket in each server.");
        System.out.println("  the rule: " + SearchLimit.TOKENS + " searches per client, refilled once an hour. client-42 sends 90 searches, dealt in turn across the servers.");
        System.out.println("  3 servers, each with its own bucket: " + burstAcrossOwnBuckets(3, 90) + " allowed, not " + SearchLimit.TOKENS + ".");
        System.out.println("  scaled out to 6 servers, the same 90: " + burstAcrossOwnBuckets(6, 90) + " allowed. every server added loosens the limit by another " + SearchLimit.TOKENS + ".");
    }

    private static int burstAcrossOwnBuckets(int serverCount, int searches) {
        List<ServerWithOwnBuckets> servers = new ArrayList<>();
        for (int i = 0; i < serverCount; i++) {
            servers.add(new ServerWithOwnBuckets());
        }
        int allowed = 0;
        for (int i = 0; i < searches; i++) {
            if (servers.get(i % serverCount).search(GREEDY)) {
                allowed++;
            }
        }
        return allowed;
    }

    /** The bucket moves into Redis. Every server asks the same place. */
    private static void two(Redis redis) {
        System.out.println("TWO. One bucket in Redis.");
        redis.forgetEverything();
        List<ServerSharingRedis> three = servers(redis, 3);
        int allowed = burst(three, GREEDY, 90);
        System.out.println("  3 servers, each with its own connection to one Redis. client-42 sends 90: " + allowed + " allowed, " + (90 - allowed) + " refused.");
        closeAll(three);

        List<ServerSharingRedis> six = servers(redis, 6);
        int allowedOnSix = burst(six, "client-77", 90);
        System.out.println("  scaled out to 6 servers, client-77 sends 90: " + allowedOnSix + " allowed. Redis holds " + redis.keys() + " keys: one bucket per client, not per server.");
        closeAll(six);

        try (ServerSharingRedis restarted = new ServerSharingRedis(redis, "server-1")) {
            ConsumptionProbe probe = restarted.searchAndHearWhen(GREEDY);
            System.out.println("  server-1 is restarted with empty memory. client-42's next search: " + (probe.isConsumed() ? "allowed" : "refused")
                    + ". retry after " + minutesRoundedUp(probe.getNanosToWaitForRefill()) + " minutes.");
        }
    }

    /** Ninety searches released at the same instant, thirty on each of three servers. */
    private static void three(Redis redis) {
        System.out.println("THREE. All at the same moment.");
        redis.forgetEverything();
        List<ServerSharingRedis> servers = servers(redis, 3);
        int allowed = allAtOnce(servers, GREEDY, 30);
        System.out.println("  3 servers, 30 searches each, all 90 released at the same instant on 90 threads: " + allowed + " allowed, " + (90 - allowed) + " refused.");
        System.out.println("  no server holds a lock. each writes its answer back only if the bucket has not changed since it read it, and reads again if it has.");
        closeAll(servers);
    }

    /**
     * Why Bucket4j does not simply keep a number in Redis. The steps of two servers are put
     * in a fixed order by hand, so the lost update happens on every run, not only on a busy day.
     */
    private static void four(Redis redis) {
        System.out.println("FOUR. Why not just a number in Redis?");
        redis.forgetEverything();
        PlainCounter counter = new PlainCounter(redis, GREEDY);
        counter.fill(1);
        int first = counter.read();
        int second = counter.read();
        int served = 0;
        if (first > 0) {
            counter.writeBlindly(first - 1);
            served++;
        }
        if (second > 0) {
            counter.writeBlindly(second - 1);
            served++;
        }
        System.out.println("  one token left. server-1 reads " + first + ". server-2 reads " + second + ". both write back " + (first - 1)
                + " and serve: " + served + " searches from 1 token. Redis now says " + counter.read() + ".");

        counter.fill(1);
        first = counter.read();
        second = counter.read();
        served = 0;
        int refused = 0;
        int triedAgain = 0;
        if (first > 0 && counter.writeIfStill(first, first - 1)) {
            served++;
        }
        if (second > 0 && !counter.writeIfStill(second, second - 1)) {
            triedAgain++;
            second = counter.read();
            if (second > 0 && counter.writeIfStill(second, second - 1)) {
                served++;
            } else {
                refused++;
            }
        }
        System.out.println("  again, but each write lands only if the number is still what was read. server-2's write is turned down; it reads again, finds "
                + second + ", and refuses. " + served + " search from 1 token, " + refused + " refused, " + triedAgain + " retry.");
        System.out.println("  Bucket4j does the second, on every search: its write is a small script that Redis runs in one step.");
    }

    /** Bucket4j does the refill sum on each server with that server's own clock. */
    private static void five(Redis redis) {
        System.out.println("FIVE. Whose clock?");
        redis.forgetEverything();
        List<ServerSharingRedis> honest = servers(redis, 2);
        int spent = burst(honest, GREEDY, 10);
        boolean honestAfter = honest.get(0).search(GREEDY);
        System.out.println("  server-1 and server-2 have correct clocks. client-42 spends " + spent + " searches through them. the next: " + (honestAfter ? "allowed" : "refused") + ".");
        int allowedFast;
        try (ServerSharingRedis fast = new ServerSharingRedis(redis, "server-3", Duration.ofHours(1))) {
            allowedFast = 0;
            for (int i = 0; i < 20; i++) {
                if (fast.search(GREEDY)) {
                    allowedFast++;
                }
            }
        }
        System.out.println("  server-3's clock runs one hour fast. client-42 sends 20 through it: " + allowedFast + " allowed. it thinks the hour is up, refills the bucket, and Redis stores its answer.");
        System.out.println("  Redis keeps the bucket. the sums are done on each server, with that server's clock. the servers' clocks must agree.");
        closeAll(honest);
    }

    /** What the shared bucket costs. */
    private static void six(Redis redis) {
        System.out.println("SIX. The bill.");
        redis.forgetEverything();
        try (ServerSharingRedis server = new ServerSharingRedis(redis, "server-1")) {
            for (int i = 1; i <= 1000; i++) {
                server.search("visitor-" + i);
            }
            System.out.println("  1000 different clients search once each: Redis holds " + redis.keys() + " keys. each is set to delete itself in "
                    + redis.minutesUntilItForgets(SearchLimit.keyFor("visitor-1")) + " minutes, when its bucket would be full again.");

            redis.stop();
            Poll.until("server-1 to notice Redis has gone", () -> !server.connected());
            int errors = 0;
            for (int i = 0; i < 5; i++) {
                try {
                    server.search(GREEDY);
                } catch (RuntimeException e) {
                    errors++;
                }
            }
            System.out.println("  Redis is stopped. 5 searches: " + errors + " errors from the limiter, and no answer. let them through, and there is no limit at all; refuse them, and "
                    + errors + " real customers see an error. the shop must choose.");
        }
        System.out.println("  and every search now waits for a trip across the network to Redis before it is served. this demo needed 1 container for 6 servers.");
    }

    private static List<ServerSharingRedis> servers(Redis redis, int count) {
        List<ServerSharingRedis> servers = new ArrayList<>();
        for (int i = 1; i <= count; i++) {
            servers.add(new ServerSharingRedis(redis, "server-" + i));
        }
        return servers;
    }

    private static void closeAll(List<ServerSharingRedis> servers) {
        servers.forEach(ServerSharingRedis::close);
    }

    /** The load balancer deals the searches to the servers in turn, one after another. */
    private static int burst(List<ServerSharingRedis> servers, String clientId, int searches) {
        int allowed = 0;
        for (int i = 0; i < searches; i++) {
            if (servers.get(i % servers.size()).search(clientId)) {
                allowed++;
            }
        }
        return allowed;
    }

    /** Every search on its own thread, all held at a gate and released together. */
    static int allAtOnce(List<ServerSharingRedis> servers, String clientId, int searchesPerServer) {
        int total = servers.size() * searchesPerServer;
        ExecutorService threads = Executors.newFixedThreadPool(total);
        try {
            CountDownLatch ready = new CountDownLatch(total);
            CountDownLatch gate = new CountDownLatch(1);
            List<Future<Boolean>> answers = new ArrayList<>();
            for (ServerSharingRedis server : servers) {
                for (int i = 0; i < searchesPerServer; i++) {
                    answers.add(threads.submit(() -> {
                        ready.countDown();
                        gate.await();
                        return server.search(clientId);
                    }));
                }
            }
            Poll.until("every thread to be waiting at the gate", () -> ready.getCount() == 0);
            gate.countDown();
            int allowed = 0;
            for (Future<Boolean> answer : answers) {
                if (answer.get(60, TimeUnit.SECONDS)) {
                    allowed++;
                }
            }
            return allowed;
        } catch (Exception e) {
            throw new IllegalStateException("the searches did not all come back", e);
        } finally {
            threads.shutdownNow();
        }
    }

    private static long minutesRoundedUp(long nanos) {
        long perMinute = 60_000_000_000L;
        return (nanos + perMinute - 1) / perMinute;
    }
}
