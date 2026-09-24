package com.jk.explore.cacheasideredis;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/** The parts that need nothing installed. These run on any machine. */
class PlainPartsTest {

    @Test
    void theCatalogueHoldsTenProductsPricedInPence() {
        Database db = Database.withTenProducts();
        assertEquals(1000, db.read("SKU-0").pricePence());
        assertEquals(1900, db.read("SKU-9").pricePence());
    }

    @Test
    void everyDatabaseReadIsCounted() {
        Database db = Database.withTenProducts();
        for (int i = 0; i < 25; i++) {
            db.read("SKU-" + (i % 10));
        }
        assertEquals(25, db.reads());
        db.resetCount();
        assertEquals(0, db.reads());
    }

    @Test
    void aProductsKeyInRedisIsNamedAfterItsSku() {
        assertEquals("product:SKU-0", RedisCache.key("SKU-0"));
    }

    @Test
    void aStampedeIsDescribedRatherThanCountedBecauseTheSchedulerDecidesTheExactNumber() {
        assertEquals("more than 40, for one price", RedisCacheAsideDemo.describeStampede(50));
        assertEquals("more than 40, for one price", RedisCacheAsideDemo.describeStampede(41));
        assertTrue(RedisCacheAsideDemo.describeStampede(12).startsWith("only 12"));
    }

    @Test
    void withNoContainerRuntimeTheAdviceIsASentenceABeginnerCanActOn() {
        assertTrue(RedisServer.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
        assertTrue(RedisServer.NO_RUNTIME_ADVICE.contains("./gradlew run"));
    }
}
