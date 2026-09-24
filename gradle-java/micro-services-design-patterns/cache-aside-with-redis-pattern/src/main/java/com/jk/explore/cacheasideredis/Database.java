package com.jk.explore.cacheasideredis;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * The source of truth for prices. Every read is counted, because reads are what the cache
 * exists to avoid.
 *
 * <p>It stays a plain object inside the shop's own program on purpose. The lesson of this
 * project is the cache, so the cache is the one thing that is real. A read can be told to take
 * a while, the way a busy database does, so that the stampede in the fifth act has time to
 * happen on its own.
 */
public class Database {

    private final Map<String, Product> rows = new HashMap<>();
    private final AtomicInteger reads = new AtomicInteger();
    private volatile long millisPerRead;

    /** The shop's ten popular products, SKU-0 to SKU-9, priced 1000 to 1900 pence. */
    public static Database withTenProducts() {
        Database db = new Database();
        for (int i = 0; i < 10; i++) {
            db.put(new Product("SKU-" + i, 1000 + i * 100));
        }
        return db;
    }

    public synchronized void put(Product p) {
        rows.put(p.sku(), p);
    }

    /** From now on every read takes this long, like a query on a busy database. */
    public void answerSlowly(long millis) {
        this.millisPerRead = millis;
    }

    public Product read(String sku) {
        reads.incrementAndGet();
        if (millisPerRead > 0) {
            try {
                Thread.sleep(millisPerRead);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        synchronized (this) {
            return rows.get(sku);
        }
    }

    public int reads() {
        return reads.get();
    }

    public void resetCount() {
        reads.set(0);
    }
}
