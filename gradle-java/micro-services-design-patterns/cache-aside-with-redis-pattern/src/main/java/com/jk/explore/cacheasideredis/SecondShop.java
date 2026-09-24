package com.jk.explore.cacheasideredis;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import redis.clients.jedis.RedisClient;

/**
 * A second shop instance, started by the demo as a separate Java program.
 *
 * <p>It has its own memory and its own copy of the catalogue, and it serves one view of each
 * of the ten products. Told {@code local}, it keeps its cache in its own memory, the way the
 * plain-Java twin did. Told {@code redis}, it uses the same Redis the first shop filled. It
 * prints one line, {@code reads=N hits=N}, which the demo reads back.
 */
public final class SecondShop {

    private SecondShop() {
    }

    public static void main(String[] args) {
        String mode = args[0];
        Database db = Database.withTenProducts();
        int hits;
        if ("local".equals(mode)) {
            hits = viewTenWithACacheInMemory(db);
        } else {
            RedisClient redis = RedisClient.create(args[1], Integer.parseInt(args[2]));
            try (RedisCache cache = new RedisCache(redis, Duration.ofSeconds(60))) {
                ProductService service = new ProductService(db, cache);
                for (int i = 0; i < 10; i++) {
                    service.get("SKU-" + i);
                }
                hits = cache.hits();
            }
        }
        System.out.println("reads=" + db.reads() + " hits=" + hits);
    }

    private static int viewTenWithACacheInMemory(Database db) {
        Map<String, Product> cache = new HashMap<>();
        int hits = 0;
        for (int i = 0; i < 10; i++) {
            String sku = "SKU-" + i;
            if (cache.containsKey(sku)) {
                hits++;
            } else {
                cache.put(sku, db.read(sku));
            }
        }
        return hits;
    }
}
