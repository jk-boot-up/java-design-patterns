package com.jk.explore.writethroughredis;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.params.SetParams;

/**
 * The pattern: every price write goes to the database, then to Redis, before it returns.
 * Reads come from Redis.
 */
public final class PriceStore {

    private final PriceDb db;
    private final Infra infra;
    private final long ttlSeconds;

    public PriceStore(PriceDb db, Infra infra, long ttlSeconds) {
        this.db = db;
        this.infra = infra;
        this.ttlSeconds = ttlSeconds;
    }

    /** Database first: if it refuses, the cache is never touched. Returns false if Redis could not be written. */
    public boolean put(String sku, int pence, boolean readOnly) throws Exception {
        db.write(sku, pence, readOnly);
        try (Jedis redis = infra.redis()) {
            redis.set("price:" + sku, Integer.toString(pence), SetParams.setParams().ex(ttlSeconds));
            return true;
        } catch (RuntimeException redisDown) {
            return false;
        }
    }

    public int get(String sku) {
        try (Jedis redis = infra.redis()) {
            return Integer.parseInt(redis.get("price:" + sku));
        }
    }
}
