package com.jk.explore.ratelimiterredis;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import io.github.bucket4j.ConsumptionProbe;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * What the shared bucket does, asked of a real Redis directly.
 *
 * <p>One Redis is started for the whole class, because starting it is the slow part, and it
 * is emptied before each test. There is no sleep anywhere in this file.
 */
class RealRedisTest {

    private static Redis redis;
    private final List<ServerSharingRedis> opened = new ArrayList<>();

    @BeforeAll
    static void startRedis() {
        assumeTrue(Redis.containerRuntimeAvailable(), "needs a container runtime");
        redis = new Redis();
        redis.start();
    }

    @AfterAll
    static void stopRedis() {
        if (redis != null) {
            redis.close();
        }
    }

    @BeforeEach
    void emptyRedis() {
        redis.forgetEverything();
    }

    @AfterEach
    void closeServers() {
        opened.forEach(ServerSharingRedis::close);
    }

    private ServerSharingRedis server(String name) {
        return server(name, Duration.ZERO);
    }

    private ServerSharingRedis server(String name, Duration clockAhead) {
        ServerSharingRedis server = new ServerSharingRedis(redis, name, clockAhead);
        opened.add(server);
        return server;
    }

    @Test
    void threeServersSharingOneBucketAllowTenBetweenThem() {
        List<ServerSharingRedis> servers = List.of(server("server-1"), server("server-2"), server("server-3"));
        int allowed = 0;
        for (int i = 0; i < 90; i++) {
            if (servers.get(i % 3).search("client-42")) {
                allowed++;
            }
        }
        assertEquals(10, allowed);
        assertEquals(1, redis.keys(), "one key for one client, however many servers");
    }

    @Test
    void ninetySearchesAtTheSameInstantStillAllowExactlyTen() {
        List<ServerSharingRedis> servers = List.of(server("server-1"), server("server-2"), server("server-3"));
        assertEquals(10, RedisRateLimiterDemo.allAtOnce(servers, "client-42", 30));
    }

    @Test
    void aRestartedServerFindsTheBucketStillEmptyAndSaysWhenToComeBack() {
        ServerSharingRedis before = server("server-1");
        for (int i = 0; i < 10; i++) {
            assertTrue(before.search("client-42"));
        }
        before.close();
        opened.remove(before);

        ConsumptionProbe probe = server("server-1").searchAndHearWhen("client-42");
        assertFalse(probe.isConsumed());
        long minutes = (probe.getNanosToWaitForRefill() + 59_999_999_999L) / 60_000_000_000L;
        assertEquals(60, minutes);
    }

    @Test
    void aPlainNumberReadAndWrittenInTwoStepsLetsTwoServersSpendTheSameToken() {
        PlainCounter counter = new PlainCounter(redis, "client-42");
        counter.fill(1);
        int first = counter.read();
        int second = counter.read();
        counter.writeBlindly(first - 1);
        counter.writeBlindly(second - 1);
        assertEquals(1, first);
        assertEquals(1, second, "both servers saw the same last token");
        assertEquals(0, counter.read(), "and Redis records one spend, not two");
    }

    @Test
    void aWriteThatLandsOnlyIfNothingChangedTurnsTheSecondServerAway() {
        PlainCounter counter = new PlainCounter(redis, "client-42");
        counter.fill(1);
        int first = counter.read();
        int second = counter.read();
        assertTrue(counter.writeIfStill(first, first - 1));
        assertFalse(counter.writeIfStill(second, second - 1));
        assertEquals(0, counter.read());
    }

    @Test
    void aServerWhoseClockRunsAnHourFastRefillsTheBucketForEveryone() {
        ServerSharingRedis honest = server("server-1");
        for (int i = 0; i < 10; i++) {
            assertTrue(honest.search("client-42"));
        }
        assertFalse(honest.search("client-42"));

        ServerSharingRedis fast = server("server-3", Duration.ofHours(1));
        int allowed = 0;
        for (int i = 0; i < 20; i++) {
            if (fast.search("client-42")) {
                allowed++;
            }
        }
        assertEquals(10, allowed);
    }

    @Test
    void redisIsToldToForgetABucketOnceItWouldBeFullAgain() {
        server("server-1").search("client-42");
        long minutes = redis.minutesUntilItForgets(SearchLimit.keyFor("client-42"));
        assertEquals(60, minutes);
    }
}
