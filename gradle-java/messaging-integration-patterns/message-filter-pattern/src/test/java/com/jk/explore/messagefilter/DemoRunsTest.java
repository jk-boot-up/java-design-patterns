package com.jk.explore.messagefilter;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", MessageFilterDemo.run());

    @Test
    void unfiltered() {
        assertTrue(all.contains("gift-wrap service handed 10 orders, wrapped [ORD-2, ORD-4]"));
    }

    @Test
    void filtered() {
        assertTrue(all.contains("receives: [ORD-2, ORD-4]; the filter dropped 8"));
        assertTrue(all.contains("loyalty bonus service receives: [ORD-1, ORD-4, ORD-6]"));
        assertTrue(all.contains("dropped: 3 guests, then 4 under £50"));
        assertTrue(all.contains("raised to £60: [ORD-1, ORD-4]"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("15 messages were dropped"));
    }
}
