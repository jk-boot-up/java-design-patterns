package com.jk.explore.cellbased;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", CellBasedDemo.run());

    @Test
    void oneStack() {
        assertTrue(all.contains("customers who could not check out: 30 of 30"));
    }

    @Test
    void cells() {
        assertTrue(all.contains("{cell-1=10, cell-2=10, cell-3=10}"));
        assertTrue(all.contains("customers who could not check out: 10 of 30"));
        assertTrue(all.contains("cell-1 rolled back: failures 0"));
        assertTrue(all.contains("6 new customers placed in cell-4; C-1 still in cell-1"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("asking all 4 cells: £1760.00"));
    }
}
