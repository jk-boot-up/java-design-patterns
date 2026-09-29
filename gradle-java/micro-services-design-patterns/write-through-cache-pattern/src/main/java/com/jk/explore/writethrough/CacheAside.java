package com.jk.explore.writethrough;

import java.util.HashMap;
import java.util.Map;

/**
 * Without the pattern: the product page reads through a cache, but price changes are written straight to the database.
 *
 * <p>Whoever changes a price must remember to clear the cache too. The
 * nightly price job did not.
 */
public final class CacheAside {

    private final Database db;
    private final Map<String, Long> cache = new HashMap<>();

    public CacheAside(Database db) {
        this.db = db;
    }

    public long pagePrice(String sku) {
        return cache.computeIfAbsent(sku, db::read);
    }

    /** The price job writes to the database and forgets the cache. */
    public void priceJobUpdate(String sku, long pence) {
        db.write(sku, pence);
    }
}
