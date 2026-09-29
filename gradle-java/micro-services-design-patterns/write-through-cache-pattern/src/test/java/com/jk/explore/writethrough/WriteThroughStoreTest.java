package com.jk.explore.writethrough;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class WriteThroughStoreTest {

    @Test
    void writeUpdatesBoth() {
        Database db = new Database();
        WriteThroughStore s = new WriteThroughStore(db);
        s.get("MUG-1");
        s.put("MUG-1", 700);
        assertEquals(700, s.get("MUG-1"));
        assertEquals(700, db.read("MUG-1"));
    }

    @Test
    void refusedWriteLeavesTheCacheAlone() {
        Database db = new Database();
        WriteThroughStore s = new WriteThroughStore(db);
        s.get("MUG-1");
        db.setReadOnly(true);
        assertThrows(IllegalStateException.class, () -> s.put("MUG-1", 1));
        assertEquals(800, s.get("MUG-1"));
    }

    @Test
    void secondReadIsAHit() {
        WriteThroughStore s = new WriteThroughStore(new Database());
        s.get("MUG-1");
        s.get("MUG-1");
        assertEquals(1, s.misses());
        assertEquals(1, s.hits());
    }

    @Test
    void cacheAsideGoesStale() {
        Database db = new Database();
        CacheAside c = new CacheAside(db);
        c.pagePrice("KETTLE-1");
        c.priceJobUpdate("KETTLE-1", 2700);
        assertEquals(3000, c.pagePrice("KETTLE-1"));
    }
}
