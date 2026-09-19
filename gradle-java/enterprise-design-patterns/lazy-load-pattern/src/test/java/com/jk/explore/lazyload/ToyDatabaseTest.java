package com.jk.explore.lazyload;

import com.jk.explore.lazyload.toydb.Database;
import com.jk.explore.lazyload.toydb.Row;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

/** The toy database is a fixture every project in the category copies, so it is proven first. */
class ToyDatabaseTest {

    @Test
    void everyOperationIsCounted() {
        Database db = new Database();
        db.table("t").insert(1, Row.of("a", 1));
        db.table("t").select(1);
        db.table("t").update(1, Row.of("a", 2));
        assertEquals(3, db.operationCount());
        assertEquals("INSERT t id=1", db.operations().get(0));
    }

    @Test
    void rowsAreStoredAsRowsAndReturnedAsCopies() {
        Database db = new Database();
        db.table("t").insert(1, Row.of("a", 1));
        Row read = db.table("t").select(1);
        read.columns().put("a", 99);
        assertEquals(1, db.table("t").peek(1).number("a"), "changing a read row must not change the table");
    }

    @Test
    void nothingIsWrittenUntilFlushWhenBuffered() {
        Database db = new Database();
        db.buffered(true);
        db.table("t").insert(1, Row.of("a", 1));
        assertNull(db.table("t").peek(1));
        assertEquals(1, db.stagedWrites());
        db.flush();
        assertEquals(1, db.table("t").peek(1).number("a"));
    }

    @Test
    void aWriteCanBeToldToFailOnDemand() {
        Database db = new Database();
        db.failWriteNumber(2);
        db.table("t").insert(1, Row.of("a", 1));
        assertThrows(IllegalStateException.class, () -> db.table("t").insert(2, Row.of("a", 2)));
        assertNull(db.table("t").peek(2));
        db.table("t").insert(3, Row.of("a", 3));
        assertEquals(1, db.table("t").peek(3).number("a") - 2);
    }
}
