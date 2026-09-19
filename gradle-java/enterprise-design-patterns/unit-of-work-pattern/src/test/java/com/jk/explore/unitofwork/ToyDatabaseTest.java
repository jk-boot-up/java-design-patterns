package com.jk.explore.unitofwork;

import com.jk.explore.unitofwork.toydb.Database;
import com.jk.explore.unitofwork.toydb.Row;
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

    @Test
    void rollbackRestoresEveryTableToTheStartOfTheTransaction() {
        Database db = new Database();
        db.table("t").insert(1, Row.of("a", 1));
        db.begin();
        db.table("t").insert(2, Row.of("a", 2));
        db.table("t").update(1, Row.of("a", 9));
        db.rollback();
        assertEquals(1, db.table("t").peek(1).number("a"));
        assertNull(db.table("t").peek(2));
    }

    @Test
    void aForeignKeyRejectsAChildWhoseParentIsMissing() {
        Database db = new Database();
        db.requireParent("lines", "order_id", "orders");
        assertThrows(IllegalStateException.class, () -> db.table("lines").insert(1, Row.of("order_id", 5)));
        db.table("orders").insert(5, Row.of("x", 1));
        db.table("lines").insert(1, Row.of("order_id", 5));
        assertEquals(5, db.table("lines").peek(1).number("order_id"));
    }
}
