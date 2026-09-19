package com.jk.explore.cacheaside;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Reads products with the cache on the side: the service looks in the cache, and on a miss goes to the
 * database itself and puts the answer in the cache. The cache never talks to the database.
 */
public class ProductService {

    private final Database db;
    private final Cache cache;
    private final ConcurrentHashMap<String, CompletableFuture<Product>> inFlight = new ConcurrentHashMap<>();

    public ProductService(Database db, Cache cache) {
        this.db = db;
        this.cache = cache;
    }

    public Product getWithoutCache(String sku) {
        return db.read(sku);
    }

    public Product get(String sku) {
        Product cached = cache.get(sku);
        if (cached != null) {
            return cached;
        }
        Product loaded = db.read(sku);
        cache.put(loaded);
        return loaded;
    }

    /** As {@link #get}, but many callers missing on the same key at once share one database read. */
    public Product getSingleFlight(String sku) {
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
            Product filledMeanwhile = cache.get(sku);
            if (filledMeanwhile != null) {
                mine.complete(filledMeanwhile);
                return filledMeanwhile;
            }
            Product loaded = db.read(sku);
            cache.put(loaded);
            mine.complete(loaded);
            return loaded;
        } finally {
            inFlight.remove(sku);
        }
    }

    /** A write goes to the database first, and then the cached copy is thrown away. */
    public void changePrice(String sku, long pence) {
        db.put(new Product(sku, pence));
        cache.invalidate(sku);
    }

    /** A write that forgets the cache. */
    public void changePriceForgettingTheCache(String sku, long pence) {
        db.put(new Product(sku, pence));
    }
}
