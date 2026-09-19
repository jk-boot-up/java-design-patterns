package com.jk.explore.cacheaside;

import java.util.ArrayList;
import java.util.List;

public class CacheAsideDemo {

    static Database database() {
        Database db = new Database();
        for (int i = 0; i < 10; i++) {
            db.put(new Product("SKU-" + i, 1000 + i * 100));
        }
        return db;
    }

    public static void main(String[] args) throws Exception {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. No cache.");
        Database db = database();
        ProductService service = new ProductService(db, new Cache(new Clock(), 60));
        for (int i = 0; i < 1000; i++) {
            service.getWithoutCache("SKU-" + (i % 10));
        }
        System.out.println("  1000 product page views over 10 popular products: " + db.reads() + " database reads.");
    }

    private static void two() {
        System.out.println("TWO. Look aside.");
        Database db = database();
        Cache cache = new Cache(new Clock(), 60);
        ProductService service = new ProductService(db, cache);
        for (int i = 0; i < 1000; i++) {
            service.get("SKU-" + (i % 10));
        }
        System.out.println("  the same 1000 views: " + db.reads() + " database reads, " + cache.hits() + " cache hits, " + cache.misses() + " misses.");
        System.out.println("  ask the cache; on a miss, ask the database and remember the answer.");
    }

    private static void three() {
        System.out.println("THREE. Writes.");
        Database db = database();
        ProductService service = new ProductService(db, new Cache(new Clock(), 60));
        service.get("SKU-0");
        service.changePriceForgettingTheCache("SKU-0", 1500);
        System.out.println("  price changed to 1500 in the database, cache forgotten: a customer sees " + service.get("SKU-0").pricePence() + ".");
        service.changePrice("SKU-0", 1600);
        System.out.println("  price changed to 1600, and the cached copy thrown away: a customer sees " + service.get("SKU-0").pricePence() + ".");
    }

    private static void four() {
        System.out.println("FOUR. A time limit on staleness.");
        Database db = database();
        Clock clock = new Clock();
        ProductService service = new ProductService(db, new Cache(clock, 60));
        service.get("SKU-0");
        db.put(new Product("SKU-0", 2000));
        clock.advance(59);
        System.out.println("  another system changes the price to 2000. after 59 seconds: " + service.get("SKU-0").pricePence() + ".");
        clock.advance(2);
        System.out.println("  after 61 seconds: " + service.get("SKU-0").pricePence() + ".");
        System.out.println("  an expiry does not make the cache right. it makes it wrong for a bounded time.");
    }

    private static void five() throws Exception {
        System.out.println("FIVE. A stampede.");
        System.out.println("  50 requests arrive together for one popular product whose entry has just expired.");
        System.out.println("  every request checks the cache: " + stampede(false) + " database reads.");
        System.out.println("  requests share one database read: " + stampede(true) + " database read.");
    }

    /** Fifty threads miss on the same key together. The database holds every read until all fifty have missed the cache. */
    static int stampede(boolean singleFlight) throws Exception {
        Database db = database();
        Cache cache = new Cache(new Clock(), 60);
        ProductService service = new ProductService(db, cache);
        int callers = 50;
        db.beforeEachRead(() -> {
            long deadline = System.nanoTime() + 10_000_000_000L;
            while (cache.misses() < callers && System.nanoTime() < deadline) {
                Thread.onSpinWait();
            }
        });
        List<Thread> threads = new ArrayList<>();
        for (int i = 0; i < callers; i++) {
            Thread t = new Thread(() -> {
                if (singleFlight) {
                    service.getSingleFlight("SKU-0");
                } else {
                    service.get("SKU-0");
                }
            });
            threads.add(t);
            t.start();
        }
        for (Thread t : threads) {
            t.join();
        }
        return db.reads();
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Database db = database();
        Cache cache = new Cache(new Clock(), 60);
        ProductService service = new ProductService(db, cache);
        for (int i = 0; i < 10; i++) {
            service.get("SKU-" + i);
        }
        db.resetCount();
        cache.clear();
        for (int i = 0; i < 10; i++) {
            service.get("SKU-" + i);
        }
        System.out.println("  the cache is restarted, empty. the first 10 views: " + db.reads() + " database reads. the database takes the whole load again until it warms up.");
        System.out.println("  the cache is a copy, not the truth. there is now a second thing to keep right, to size, and to explain.");
    }
}
