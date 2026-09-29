package com.jk.explore.processcamel;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", CamelProcessManagerDemo.run());
        assertTrue(all.contains("kettles in stock: 1 of 3, though only one was shipped"));
        assertTrue(all.contains("ORD-1 replies: [main RESERVED, PAID, SHIPPED] -> DONE"));
        assertTrue(all.contains("ORD-2 replies: [main OUT_OF_STOCK, partner RESERVED, PAID, SHIPPED] -> DONE"));
        assertTrue(all.contains("ORD-3 replies: [main RESERVED, DECLINED, main RELEASED]"));
        assertTrue(all.contains("-> CANCELLED, stock released; kettles in stock: 2 of 3"));
        assertTrue(all.contains("email: [ORD-3: your card was declined]"));
        assertTrue(all.contains("{ORD-1=DONE, ORD-2=DONE, ORD-3=CANCELLED, stock released}"));
    }
}
