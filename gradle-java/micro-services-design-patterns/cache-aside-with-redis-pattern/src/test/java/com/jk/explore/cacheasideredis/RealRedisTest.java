package com.jk.explore.cacheasideredis;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.time.Duration;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * What the real Redis does, asked of it directly.
 *
 * <p>One Redis is started for the whole class, because starting it is the slow part, and it is
 * emptied before each test. Every wait here is a bounded poll on something Redis can actually
 * be asked about — whether a key still exists. There is no sleep anywhere in this file.
 */
class RealRedisTest {

    private static RedisServer redis;

    @BeforeAll
    static void startRedis() {
        assumeTrue(RedisServer.containerRuntimeAvailable(), "needs a container runtime");
        redis = new RedisServer();
        redis.start();
    }

    @AfterAll
    static void stopRedis() {
        if (redis != null) {
            redis.close();
        }
    }

    @BeforeEach
    void empty() {
        redis.cli("FLUSHALL");
    }

    @Test
    void aMissReadsTheDatabaseOnceAndEveryLaterViewIsAHit() {
        Database db = Database.withTenProducts();
        try (RedisCache cache = new RedisCache(redis.connect(), Duration.ofSeconds(60))) {
            ProductService shop = new ProductService(db, cache);
            for (int i = 0; i < 100; i++) {
                assertEquals(1000, shop.get("SKU-0").pricePence());
            }
            assertEquals(1, db.reads());
            assertEquals(99, cache.hits());
            assertEquals(1, cache.misses());
        }
    }

    @Test
    void anotherConnectionSeesWhatTheFirstOneWrote() {
        try (RedisCache first = new RedisCache(redis.connect(), Duration.ofSeconds(60));
             RedisCache second = new RedisCache(redis.connect(), Duration.ofSeconds(60))) {
            first.put(new Product("SKU-3", 1300));
            assertEquals(1300, second.get("SKU-3").pricePence());
            assertEquals("1300", redis.cli("GET", "product:SKU-3"));
        }
    }

    @Test
    void aSecondJavaProcessFindsTheCacheAlreadyWarm() {
        Database db = Database.withTenProducts();
        try (RedisCache cache = new RedisCache(redis.connect(), Duration.ofSeconds(60))) {
            ProductService first = new ProductService(db, cache);
            for (int i = 0; i < 10; i++) {
                first.get("SKU-" + i);
            }
        }
        RedisCacheAsideDemo.SecondShopResult local = RedisCacheAsideDemo.startSecondShop("local", redis);
        RedisCacheAsideDemo.SecondShopResult shared = RedisCacheAsideDemo.startSecondShop("redis", redis);
        assertEquals(new RedisCacheAsideDemo.SecondShopResult(10, 0), local);
        assertEquals(new RedisCacheAsideDemo.SecondShopResult(0, 10), shared);
    }

    @Test
    void aChangedPriceIsSeenAfterTheCachedCopyIsDeleted() {
        Database db = Database.withTenProducts();
        try (RedisCache cache = new RedisCache(redis.connect(), Duration.ofSeconds(60))) {
            ProductService shop = new ProductService(db, cache);
            shop.get("SKU-0");
            shop.changePrice("SKU-0", 1600);
            assertFalse(cache.holds("SKU-0"));
            assertEquals(1600, shop.get("SKU-0").pricePence());
        }
    }

    @Test
    void redisRemovesAnExpiredEntryOnItsOwnClock() {
        try (RedisCache cache = new RedisCache(redis.connect(), Duration.ofMillis(300))) {
            cache.put(new Product("SKU-0", 1000));
            assertTrue(cache.holds("SKU-0"));
            Poll.until("Redis to remove the entry", Duration.ofSeconds(10), () -> !cache.holds("SKU-0"));
            assertNull(cache.get("SKU-0"));
            assertEquals(-2, cache.secondsToLive("SKU-0"));
        }
    }

    @Test
    void aPlainSetThrowsTheExpiryAway() {
        try (RedisCache cache = new RedisCache(redis.connect(), Duration.ofSeconds(60))) {
            cache.put(new Product("SKU-0", 1000));
            long before = cache.secondsToLive("SKU-0");
            assertTrue(before > 0 && before <= 60, "an expiry was set: " + before);
            cache.putWithoutExpiry(new Product("SKU-0", 2000));
            assertEquals(-1, cache.secondsToLive("SKU-0"));
        }
    }

    @Test
    void onlyOneCallerGetsTheLockUntilItIsLetGo() {
        try (RedisCache a = new RedisCache(redis.connect(), Duration.ofSeconds(60));
             RedisCache b = new RedisCache(redis.connect(), Duration.ofSeconds(60))) {
            assertTrue(a.tryLock("SKU-0", Duration.ofSeconds(5)));
            assertFalse(b.tryLock("SKU-0", Duration.ofSeconds(5)));
            a.unlock("SKU-0");
            assertTrue(b.tryLock("SKU-0", Duration.ofSeconds(5)));
        }
    }

    @Test
    void aLockWhoseHolderDiedExpiresByItself() {
        try (RedisCache a = new RedisCache(redis.connect(), Duration.ofSeconds(60));
             RedisCache b = new RedisCache(redis.connect(), Duration.ofSeconds(60))) {
            assertTrue(a.tryLock("SKU-0", Duration.ofMillis(300)));
            Poll.until("the lock to expire", Duration.ofSeconds(10), () -> b.tryLock("SKU-0", Duration.ofSeconds(5)));
        }
    }

    /**
     * How many of the fifty reach the database is up to the thread scheduler, so the test
     * asserts a range. The two answers are exact, because they are guaranteed by the code.
     */
    @Test
    void aStampedeHitsTheDatabaseManyTimesAndALockInRedisBringsItToOne() {
        int everyone = RedisCacheAsideDemo.stampede(redis, ProductService::get);
        assertTrue(everyone > 40 && everyone <= 50, "reads: " + everyone);
        assertEquals(2, RedisCacheAsideDemo.stampede(redis, ProductService::getSharingInsideThisInstance));
        assertEquals(1, RedisCacheAsideDemo.stampede(redis, ProductService::getSharingThroughRedis));
    }

    @Test
    void outOfTheBoxRedisHasNoMemoryLimitAndEvictsNothing() {
        assertEquals("maxmemory\n0", redis.cli("CONFIG", "GET", "maxmemory"));
        assertEquals("maxmemory-policy\nnoeviction", redis.cli("CONFIG", "GET", "maxmemory-policy"));
    }
}
