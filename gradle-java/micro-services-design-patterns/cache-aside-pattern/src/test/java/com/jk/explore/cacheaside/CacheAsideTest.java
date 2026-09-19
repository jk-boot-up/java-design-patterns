package com.jk.explore.cacheaside;

import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class CacheAsideTest {

    @Test
    void withoutACacheEveryViewIsADatabaseRead() {
        Database db = CacheAsideDemo.database();
        ProductService s = new ProductService(db, new Cache(new Clock(), 60));
        for (int i = 0; i < 100; i++) s.getWithoutCache("SKU-" + (i % 10));
        assertEquals(100, db.reads());
    }

    @Test
    void cacheAsideReadsEachProductOnce() {
        Database db = CacheAsideDemo.database();
        Cache c = new Cache(new Clock(), 60);
        ProductService s = new ProductService(db, c);
        for (int i = 0; i < 1000; i++) s.get("SKU-" + (i % 10));
        assertEquals(10, db.reads());
        assertEquals(990, c.hits());
        assertEquals(10, c.misses());
    }

    @Test
    void aWriteThatForgetsTheCacheServesStaleDataUntilInvalidated() {
        ProductService s = new ProductService(CacheAsideDemo.database(), new Cache(new Clock(), 60));
        s.get("SKU-0");
        s.changePriceForgettingTheCache("SKU-0", 1500);
        assertEquals(1000, s.get("SKU-0").pricePence());
        s.changePrice("SKU-0", 1600);
        assertEquals(1600, s.get("SKU-0").pricePence());
    }

    @Test
    void anEntryExpiresExactlyAtItsTimeToLive() {
        Database db = CacheAsideDemo.database();
        Clock clock = new Clock();
        ProductService s = new ProductService(db, new Cache(clock, 60));
        s.get("SKU-0");
        db.put(new Product("SKU-0", 2000));
        clock.advance(59);
        assertEquals(1000, s.get("SKU-0").pricePence());
        clock.advance(1);
        assertEquals(2000, s.get("SKU-0").pricePence());
    }

    @Test
    void anEmptiedCacheSendsTheWholeLoadBackToTheDatabase() {
        Database db = CacheAsideDemo.database();
        Cache c = new Cache(new Clock(), 60);
        ProductService s = new ProductService(db, c);
        for (int i = 0; i < 10; i++) s.get("SKU-" + i);
        db.resetCount();
        c.clear();
        for (int i = 0; i < 10; i++) s.get("SKU-" + i);
        assertEquals(10, db.reads());
    }

    @RepeatedTest(5)
    void aStampedeReadsTheDatabaseOncePerCallerUnlessReadsAreShared() throws Exception {
        assertEquals(50, CacheAsideDemo.stampede(false));
        assertEquals(1, CacheAsideDemo.stampede(true));
    }
}
