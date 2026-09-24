package com.jk.explore.cacheasideredis;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.function.BiFunction;

/**
 * Six acts against a real Redis server, started and stopped by this program.
 *
 * <p>The shop shows product pages, and every page needs a price from the database. The first
 * act reads the database every time. The rest put Redis on the side and show what a cache in
 * its own process does that a cache inside the shop cannot: be seen by another process, expire
 * on its own clock, and be stampeded for real.
 */
public class RedisCacheAsideDemo {

    static final Duration AN_HOUR_OF_SHOPPING = Duration.ofSeconds(60);
    static final Duration SHORT_LIFE = Duration.ofSeconds(2);
    static final int TOGETHER = 50;
    static final long SLOW_READ_MILLIS = 500;

    public static void main(String[] args) {
        if (!RedisServer.containerRuntimeAvailable()) {
            System.out.println(RedisServer.NO_RUNTIME_ADVICE);
            return;
        }
        try (RedisServer redis = new RedisServer()) {
            try {
                redis.start();
            } catch (RuntimeException e) {
                System.out.println(RedisServer.WOULD_NOT_START_ADVICE);
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

    /** Every page view reads the database. */
    private static void one() {
        System.out.println("ONE. No cache.");
        Database db = Database.withTenProducts();
        for (int i = 0; i < 1000; i++) {
            db.read("SKU-" + (i % 10));
        }
        System.out.println("  1000 product page views over 10 popular products: " + db.reads() + " database reads.");
    }

    /** Redis on the side. The shop asks it first, and fills it on a miss. */
    private static void two(RedisServer redis) {
        System.out.println("TWO. Look aside, in Redis.");
        redis.cli("FLUSHALL");
        Database db = Database.withTenProducts();
        try (RedisCache cache = new RedisCache(redis.connect(), AN_HOUR_OF_SHOPPING)) {
            ProductService shop = new ProductService(db, cache);
            for (int i = 0; i < 1000; i++) {
                shop.get("SKU-" + (i % 10));
            }
            System.out.println("  a Redis server is running in a container. the same 1000 views: " + db.reads() + " database reads, " + cache.hits() + " cache hits, " + cache.misses() + " misses.");
            System.out.println("  Redis now holds " + redis.cli("DBSIZE") + " keys, each written with a " + AN_HOUR_OF_SHOPPING.toSeconds() + " second expiry.");
        }
    }

    /** A second shop, in a separate process, and Redis's own command-line program. */
    private static void three(RedisServer redis) {
        System.out.println("THREE. Another process can see it.");
        redis.cli("FLUSHALL");
        Database db = Database.withTenProducts();
        try (RedisCache cache = new RedisCache(redis.connect(), AN_HOUR_OF_SHOPPING)) {
            ProductService first = new ProductService(db, cache);
            for (int i = 0; i < 10; i++) {
                first.get("SKU-" + i);
            }
            SecondShopResult local = startSecondShop("local", redis);
            System.out.println("  the first shop has viewed all 10 products. a second shop starts as a separate Java process.");
            System.out.println("  with its cache in its own memory, its first 10 views: " + local.reads() + " database reads, " + local.hits() + " cache hits.");
            SecondShopResult shared = startSecondShop("redis", redis);
            System.out.println("  with its cache in Redis, its first 10 views: " + shared.reads() + " database reads, " + shared.hits() + " cache hits.");
            System.out.println("  redis-cli, a separate program in the container, asks for " + RedisCache.key("SKU-0") + " and is told: " + redis.cli("GET", RedisCache.key("SKU-0")) + ".");
            first.changePrice("SKU-0", 1600);
            System.out.println("  the first shop changes SKU-0 to 1600 and deletes the key once. copies left for any process: " + redis.cli("EXISTS", RedisCache.key("SKU-0")) + ".");
        }
    }

    /** Expiry on Redis's own clock, and the plain write that switches it off. */
    private static void four(RedisServer redis) {
        System.out.println("FOUR. Real expiry.");
        redis.cli("FLUSHALL");
        Database db = Database.withTenProducts();
        try (RedisCache cache = new RedisCache(redis.connect(), SHORT_LIFE)) {
            ProductService shop = new ProductService(db, cache);
            shop.get("SKU-0");
            db.put(new Product("SKU-0", 2000));
            System.out.println("  SKU-0 is cached for " + SHORT_LIFE.toSeconds() + " seconds. another system changes the price to 2000. a customer sees " + shop.get("SKU-0").pricePence() + ".");
            Poll.until("Redis to remove the entry by itself", () -> !cache.holds("SKU-0"));
            System.out.println("  nobody deletes it. Redis removes the key itself when the time is up. a customer then sees " + shop.get("SKU-0").pricePence() + ".");

            cache.putWithoutExpiry(new Product("SKU-0", 2000));
            System.out.println("  a price-sync job writes SKU-0 again with a plain SET. seconds to live, as Redis reports it: " + cache.secondsToLive("SKU-0") + ", which means never.");
            db.put(new Product("SKU-0", 2100));
            try (RedisCache marker = new RedisCache(redis.connect(), SHORT_LIFE)) {
                marker.put(new Product("SKU-MARKER", 0));
                Poll.until("an entry given the same " + SHORT_LIFE.toSeconds() + " seconds to expire", () -> !marker.holds("SKU-MARKER"));
            }
            System.out.println("  the price changes to 2100. " + SHORT_LIFE.toSeconds() + " seconds later a customer still sees " + shop.get("SKU-0").pricePence() + ". the entry will never expire.");
            System.out.println("  an expiry only limits staleness while every write keeps it. one plain write turned it off.");
        }
    }

    /** Fifty requests together, on two shop instances, for an entry that has just gone. */
    private static void five(RedisServer redis) {
        System.out.println("FIVE. A real stampede.");
        System.out.println("  " + TOGETHER + " requests arrive together, across 2 shop instances, for SKU-0 just after its entry expired. a database read takes " + SLOW_READ_MILLIS + " milliseconds.");
        int everyone = stampede(redis, ProductService::get);
        System.out.println("  every request checks Redis and misses. database reads: " + describeStampede(everyone) + ".");
        int perInstance = stampede(redis, ProductService::getSharingInsideThisInstance);
        System.out.println("  requests share a read inside each instance: " + perInstance + " database reads, one per instance.");
        int throughRedis = stampede(redis, ProductService::getSharingThroughRedis);
        System.out.println("  requests share a lock kept in Redis: " + throughRedis + " database read. the lock expires by itself after " + ProductService.LOCK_HELD_AT_MOST.toSeconds() + " seconds if its holder dies.");
    }

    /**
     * How many of the fifty went to the database. Which exact number is up to the thread
     * scheduler, so it is printed as a description rather than a count.
     */
    static String describeStampede(int reads) {
        if (reads > 40) {
            return "more than 40, for one price";
        }
        return "only " + reads + ", fewer than usual, for one price";
    }

    /** Runs fifty requests at once, half on each of two shop instances, and counts database reads. */
    static int stampede(RedisServer redis, BiFunction<ProductService, String, Product> read) {
        redis.cli("FLUSHALL");
        Database db = Database.withTenProducts();
        db.answerSlowly(SLOW_READ_MILLIS);
        try (RedisCache cacheA = new RedisCache(redis.connect(), AN_HOUR_OF_SHOPPING);
             RedisCache cacheB = new RedisCache(redis.connect(), AN_HOUR_OF_SHOPPING)) {
            ProductService[] shops = {new ProductService(db, cacheA), new ProductService(db, cacheB)};
            CountDownLatch go = new CountDownLatch(1);
            List<Thread> threads = new ArrayList<>();
            for (int i = 0; i < TOGETHER; i++) {
                ProductService shop = shops[i % 2];
                Thread t = new Thread(() -> {
                    try {
                        go.await();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }
                    read.apply(shop, "SKU-0");
                });
                threads.add(t);
                t.start();
            }
            go.countDown();
            for (Thread t : threads) {
                t.join(TimeUnit.SECONDS.toMillis(30));
            }
            return db.reads();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    /** What the cache costs. */
    private static void six(RedisServer redis) {
        System.out.println("SIX. The bill.");
        redis.cli("FLUSHALL");
        Database db = Database.withTenProducts();
        try (RedisCache cache = new RedisCache(redis.connect(), AN_HOUR_OF_SHOPPING)) {
            ProductService shop = new ProductService(db, cache);
            for (int i = 0; i < 10; i++) {
                shop.get("SKU-" + i);
            }
            System.out.println("  Redis is emptied, as a restart with nothing saved leaves it. the first 10 views: " + db.reads() + " database reads.");
            String limit = redis.cli("CONFIG", "GET", "maxmemory").split("\\s+")[1];
            String policy = redis.cli("CONFIG", "GET", "maxmemory-policy").split("\\s+")[1];
            System.out.println("  Redis out of the box: maxmemory " + limit + ", which means no limit, and maxmemory-policy " + policy + ".");
            System.out.println("  a cache must be given a size and told what to throw away, or it grows until the machine runs out.");
            System.out.println("  and a price now crosses the network as text: Redis holds SKU-0 as the string " + redis.cli("GET", RedisCache.key("SKU-0")) + ".");
            System.out.println("  and Redis is one more system to run, secure and watch: this demo needed 1 container for 2 shop processes.");
        }
    }

    record SecondShopResult(int reads, int hits) {
    }

    /** Starts {@link SecondShop} as a separate Java process and reads back its one line. */
    static SecondShopResult startSecondShop(String mode, RedisServer redis) {
        String java = Path.of(System.getProperty("java.home"), "bin", "java").toString();
        ProcessBuilder builder = new ProcessBuilder(java, "-cp", System.getProperty("java.class.path"),
                SecondShop.class.getName(), mode, redis.host(), Integer.toString(redis.port()));
        builder.redirectErrorStream(true);
        try {
            Process process = builder.start();
            String out = new String(process.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
            if (!process.waitFor(60, TimeUnit.SECONDS) || process.exitValue() != 0) {
                throw new IllegalStateException("the second shop did not finish: " + out);
            }
            String line = out.lines().filter(l -> l.startsWith("reads=")).findFirst()
                    .orElseThrow(() -> new IllegalStateException("the second shop said: " + out));
            String[] parts = line.split(" ");
            return new SecondShopResult(Integer.parseInt(parts[0].substring(6)), Integer.parseInt(parts[1].substring(5)));
        } catch (IOException e) {
            throw new IllegalStateException(e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }
}
