package com.jk.explore.processmanager;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", ProcessManagerDemo.run());

    @Test
    void chained() {
        assertTrue(all.contains("kettles in stock: 1 of 3, though only one was shipped"));
    }

    @Test
    void manager() {
        assertTrue(all.contains("ORD-1 replies: [main RESERVED, PAID, SHIPPED] -> DONE"));
        assertTrue(all.contains("ORD-2 replies: [main OUT_OF_STOCK, partner RESERVED, PAID, SHIPPED] -> DONE"));
        assertTrue(all.contains("stock released; kettles in stock: 2 of 3"));
    }
}
