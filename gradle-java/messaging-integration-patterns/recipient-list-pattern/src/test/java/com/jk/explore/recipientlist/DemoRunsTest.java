package com.jk.explore.recipientlist;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", RecipientListDemo.run());

    @Test
    void broadcast() {
        assertTrue(all.contains("5 orders x 4 warehouses = 20 deliveries; 8 of them needed"));
    }

    @Test
    void list() {
        assertTrue(all.contains("ORD-1 [kitchen, furniture] -> [north, big-items]"));
        assertTrue(all.contains("ORD-4 (£650.00) -> [big-items, cold-store, fraud-review]"));
        assertTrue(all.contains("ORD-2 (a gift)  -> [north, gift-wrap]"));
        assertTrue(all.contains("ORD-5 -> [south, cold-store]"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("ORD-1 reached [south], failed [big-items]"));
    }
}
