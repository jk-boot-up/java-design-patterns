package com.jk.explore.recipientcamel;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", CamelRecipientListDemo.run());
        assertTrue(all.contains("5 orders x 4 warehouses = 20 deliveries"));
        assertTrue(all.contains("ORD-4 [furniture, chilled] -> big-items,cold-store,fraud-review"));
        assertTrue(all.contains("deliveries: 10"));
        assertTrue(all.contains("ORD-2 (a gift)  reached [north, gift-wrap]"));
        assertTrue(all.contains("ORD-5 reached [south, cold-store]"));
        assertTrue(all.contains("Camel reports: big-items is unreachable"));
        assertTrue(all.contains("ORD-1 still reached [south]"));
    }
}
