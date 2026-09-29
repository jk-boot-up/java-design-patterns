package com.jk.explore.cellbased;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;

import java.util.List;
import org.junit.jupiter.api.Test;

class CellRouterTest {

    private CellRouter threeCells() {
        CellRouter r = new CellRouter();
        r.addCell(new Cell("a"));
        r.addCell(new Cell("b"));
        r.addCell(new Cell("c"));
        r.place(CellBasedDemo.CUSTOMERS);
        return r;
    }

    @Test
    void customersStayInTheirCell() {
        CellRouter r = threeCells();
        assertSame(r.cellOf("C-4"), r.cellOf("C-4"));
        assertEquals("a", r.cellOf("C-1").name());
        assertEquals("b", r.cellOf("C-2").name());
    }

    @Test
    void badReleaseHitsOneThird() {
        CellRouter r = threeCells();
        r.cells().get(1).deploy("v2-buggy");
        assertEquals(10, CellBasedDemo.failures(r, CellBasedDemo.CUSTOMERS));
    }

    @Test
    void newCustomersGoToTheNewCell() {
        CellRouter r = threeCells();
        Cell d = new Cell("d");
        r.addCell(d);
        r.sendNewCustomersTo(d);
        assertSame(d, r.cellOf("C-99"));
        assertEquals("a", r.cellOf("C-1").name());
    }

    @Test
    void salesAreSplitAcrossCells() {
        CellRouter r = threeCells();
        CellBasedDemo.failures(r, List.of("C-1", "C-2", "C-3"));
        assertEquals(2000, r.cells().get(0).salesPence());
    }
}
