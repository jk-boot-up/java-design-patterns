package com.jk.explore.cacheasideredis;

import java.time.Duration;
import java.util.concurrent.atomic.AtomicInteger;
import redis.clients.jedis.RedisClient;
import redis.clients.jedis.params.SetParams;

/**
 * Prices kept in Redis, one key per product: the key {@code product:SKU-0} holds the text
 * {@code 1000}.
 *
 * <p>Redis stores text, not Java objects, so a price goes in as a string of digits and comes
 * back out as one. Every entry is written with an expiry — Redis calls the time an entry has
 * left its TTL, its time to live — and Redis removes the entry by itself when that time is up.
 * This class counts hits and misses for this one shop instance only; Redis does not know or
 * care which instance asked.
 */
public class RedisCache implements AutoCloseable {

    private final RedisClient redis;
    private final Duration timeToLive;
    private final AtomicInteger hits = new AtomicInteger();
    private final AtomicInteger misses = new AtomicInteger();

    public RedisCache(RedisClient redis, Duration timeToLive) {
        this.redis = redis;
        this.timeToLive = timeToLive;
    }

    public static String key(String sku) {
        return "product:" + sku;
    }

    private static String lockKey(String sku) {
        return "lock:" + key(sku);
    }

    /** The cached product, or null when Redis has no entry for it. Counts a hit or a miss. */
    public Product get(String sku) {
        Product found = peek(sku);
        if (found == null) {
            misses.incrementAndGet();
        } else {
            hits.incrementAndGet();
        }
        return found;
    }

    /** Looks without counting, for a request that is only waiting for somebody else's fill. */
    public Product peek(String sku) {
        String text = redis.get(key(sku));
        return text == null ? null : new Product(sku, Long.parseLong(text));
    }

    /** Writes the price with this cache's expiry, in one command: SET key value PX millis. */
    public void put(Product p) {
        redis.set(key(p.sku()), Long.toString(p.pricePence()), SetParams.setParams().px(timeToLive.toMillis()));
    }

    /**
     * Writes the price with a plain SET and nothing else. Redis treats that as a brand new
     * value with no expiry at all, and throws away any expiry the key had before.
     */
    public void putWithoutExpiry(Product p) {
        redis.set(key(p.sku()), Long.toString(p.pricePence()));
    }

    public void forget(String sku) {
        redis.del(key(sku));
    }

    public boolean holds(String sku) {
        return redis.exists(key(sku));
    }

    /** Seconds left before Redis removes the entry; -1 means never, -2 means it is not there. */
    public long secondsToLive(String sku) {
        return redis.ttl(key(sku));
    }

    /**
     * Tries to take a lock that every shop instance can see: SET lock:key held NX PX millis.
     * NX means "only if nobody has set it already", so exactly one caller gets "OK". The lock
     * has its own expiry, so a shop that dies holding it cannot block the others for ever.
     */
    public boolean tryLock(String sku, Duration holdFor) {
        String answer = redis.set(lockKey(sku), "held", SetParams.setParams().nx().px(holdFor.toMillis()));
        return "OK".equals(answer);
    }

    public void unlock(String sku) {
        redis.del(lockKey(sku));
    }

    public int hits() {
        return hits.get();
    }

    public int misses() {
        return misses.get();
    }

    @Override
    public void close() {
        redis.close();
    }
}
