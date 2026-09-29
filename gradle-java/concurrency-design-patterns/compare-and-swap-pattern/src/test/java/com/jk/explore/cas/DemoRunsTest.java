package com.jk.explore.cas;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", CompareAndSwapDemo.run());
    }

    @Test
    void unsafeOversells() {
        assertTrue(all.contains("kettles sold: more than 100, from a stock of 100"));
    }

    @Test
    void safeWays() {
        assertTrue(all.contains("kettles sold: 100; left: 0"));
        assertTrue(all.contains("sold 100, left 0"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("stock 99, buyers recorded 0"));
    }
}
