package com.jk.explore.spacebased;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", SpaceBasedDemo.run());
    }

    @Test
    void central() {
        assertTrue(all.contains("300 kettle orders: over 1.4 s"));
        assertTrue(all.contains("six app servers: still over 1.4 s"));
    }

    @Test
    void units() {
        assertTrue(all.contains("300 orders in under 0.3 s"));
        assertTrue(all.contains("[unit-1 900, unit-2 900, unit-3 900]"));
        assertTrue(all.contains("after replication: [unit-1 700, unit-2 700, unit-3 700]"));
        assertTrue(all.contains("database stock now 700, written in 3 batches"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("unit-1 sold: true, unit-2 sold: true; stock after replication: -1"));
    }
}
