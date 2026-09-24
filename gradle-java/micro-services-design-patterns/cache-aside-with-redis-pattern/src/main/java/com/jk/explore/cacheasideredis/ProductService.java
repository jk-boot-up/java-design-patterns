package com.jk.explore.cacheasideredis;

import java.time.Duration;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;

/**
 * One shop instance reading prices with the cache on the side. The service looks in Redis
 * first; on a miss it goes to the database itself and writes the answer into Redis. Redis
 * never talks to the database. That is the whole pattern.
 */
public class ProductService {

    /** How long the lock that guards a refill is held at most, if its holder dies. */
    static final Duration LOCK_HELD_AT_MOST = Duration.ofSeconds(5);

    private final Database db;
    private final RedisCache cache;
    private final ConcurrentHashMap<String, CompletableFuture<Product>> inFlight = new ConcurrentHashMap<>();

    public ProductService(Database db, RedisCache cache) {
        this.db = db;
        this.cache = cache;
    }

    public Product getWithoutCache(String sku) {
        return db.read(sku);
    }

    /** Cache-aside: ask Redis; on a miss, ask the database and remember the answer in Redis. */
    public Product get(String sku) {
        Product cached = cache.get(sku);
        if (cached != null) {
            return cached;
        }
        Product loaded = db.read(sku);
        cache.put(loaded);
        return loaded;
    }

    /**
     * As {@link #get}, but requests inside this one instance that miss at the same time share
     * one database read. Another instance knows nothing about it and does its own.
     */
    public Product getSharingInsideThisInstance(String sku) {
        Product cached = cache.get(sku);
        if (cached != null) {
            return cached;
        }
        CompletableFuture<Product> mine = new CompletableFuture<>();
        CompletableFuture<Product> existing = inFlight.putIfAbsent(sku, mine);
        if (existing != null) {
            return existing.join();
        }
        try {
            Product filledMeanwhile = cache.peek(sku);
            Product result = filledMeanwhile != null ? filledMeanwhile : loadAndRemember(sku);
            mine.complete(result);
            return result;
        } finally {
            inFlight.remove(sku);
        }
    }

    /**
     * As {@link #get}, but on a miss the request first tries to take a lock in Redis. Only the
     * one that gets it reads the database. Everyone else, in this instance or any other, waits
     * for the entry to appear in Redis.
     */
    public Product getSharingThroughRedis(String sku) {
        Product cached = cache.get(sku);
        if (cached != null) {
            return cached;
        }
        while (true) {
            if (cache.tryLock(sku, LOCK_HELD_AT_MOST)) {
                try {
                    Product filledMeanwhile = cache.peek(sku);
                    return filledMeanwhile != null ? filledMeanwhile : loadAndRemember(sku);
                } finally {
                    cache.unlock(sku);
                }
            }
            Product[] seen = new Product[1];
            try {
                Poll.until("another request to fill " + sku, LOCK_HELD_AT_MOST.plusSeconds(1),
                        () -> (seen[0] = cache.peek(sku)) != null);
                return seen[0];
            } catch (IllegalStateException holderDied) {
                // The lock's own expiry has passed without a fill. Try to take it again.
            }
        }
    }

    private Product loadAndRemember(String sku) {
        Product loaded = db.read(sku);
        cache.put(loaded);
        return loaded;
    }

    /** A write goes to the database first, and then the cached copy is thrown away. */
    public void changePrice(String sku, long pence) {
        db.put(new Product(sku, pence));
        cache.forget(sku);
    }
}
