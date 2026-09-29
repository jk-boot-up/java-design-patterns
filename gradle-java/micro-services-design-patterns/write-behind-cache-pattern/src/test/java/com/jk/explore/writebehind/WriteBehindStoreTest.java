package com.jk.explore.writebehind;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Map;
import org.junit.jupiter.api.Test;

class WriteBehindStoreTest {

    private final Database db = new Database();
    private final WriteBehindStore store = new WriteBehindStore(db);

    @Test
    void changesAreReadableAtOnceButNotWritten() {
        assertEquals(0, store.set("c", "mug", 2));
        assertEquals(Map.of("mug", 2), store.get("c"));
        assertEquals(0, db.writes());
    }

    @Test
    void flushWritesEachCartOnce() {
        for (int n = 1; n <= 5; n++) {
            store.set("c", "mug", n);
        }
        assertEquals(1, store.flush());
        assertEquals(Map.of("mug", 5), db.load("c"));
    }

    @Test
    void quantityZeroRemovesTheItem() {
        store.set("c", "mug", 2);
        store.set("c", "mug", 0);
        store.flush();
        assertEquals(Map.of(), db.load("c"));
    }

    @Test
    void failedFlushKeepsCartsDirty() {
        store.set("c", "mug", 1);
        db.setUp(false);
        assertEquals(-1, store.flush());
        assertEquals(1, store.waiting());
        db.setUp(true);
        assertEquals(1, store.flush());
        assertEquals(0, store.waiting());
    }

    @Test
    void crashLosesUnflushedChanges() {
        store.set("c", "mug", 1);
        store.flush();
        store.set("c", "mug", 4);
        assertEquals(1, store.crash());
        assertEquals(Map.of("mug", 1), db.load("c"));
    }

    @Test
    void writeThroughWritesEveryChange() {
        WriteThroughStore wt = new WriteThroughStore(db);
        assertEquals(20, wt.set("c", "mug", 1));
        wt.set("c", "mug", 2);
        assertEquals(2, db.writes());
    }
}
