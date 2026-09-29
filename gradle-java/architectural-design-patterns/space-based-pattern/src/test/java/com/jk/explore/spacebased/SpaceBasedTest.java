package com.jk.explore.spacebased;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class SpaceBasedTest {

    @Test
    void replicationBringsEveryCopyInStep() {
        CentralDatabase db = new CentralDatabase(10);
        DataGrid grid = new DataGrid(new DataWriter(db, 100));
        ProcessingUnit a = new ProcessingUnit("a", 10, grid);
        ProcessingUnit b = new ProcessingUnit("b", 10, grid);
        grid.join(a);
        grid.join(b);
        a.takeOne();
        a.takeOne();
        b.takeOne();
        assertEquals(8, a.stock());
        assertEquals(9, b.stock());
        grid.flush();
        assertEquals(7, a.stock());
        assertEquals(7, b.stock());
        assertEquals(7, db.stock());
    }

    @Test
    void writerBatches() {
        CentralDatabase db = new CentralDatabase(1000);
        DataWriter w = new DataWriter(db, 10);
        for (int i = 0; i < 25; i++) {
            w.record(1);
        }
        w.flush();
        assertEquals(3, db.writes());
        assertEquals(975, db.stock());
    }

    @Test
    void unitRefusesWhenItsCopyIsEmpty() {
        DataGrid grid = new DataGrid(new DataWriter(new CentralDatabase(0), 10));
        ProcessingUnit u = new ProcessingUnit("u", 0, grid);
        grid.join(u);
        assertEquals(false, u.takeOne());
    }
}
