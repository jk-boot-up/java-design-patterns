package com.jk.explore.statetable;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", StateTableDemo.run());

    @Test
    void ifElseBugs() {
        assertTrue(all.contains("cancel a delivered order: allowed, now CANCELLED"));
        assertTrue(all.contains("allowed, 2 refunds of £63.44"));
    }

    @Test
    void tablePrinted() {
        assertTrue(all.contains("PLACED: PAY -> PAID, CANCEL -> CANCELLED"));
        assertTrue(all.contains("ORD-1: [PLACED, PAID, SHIPPED, DELIVERED]"));
    }

    @Test
    void refusals() {
        assertTrue(all.contains("refused, cannot cancel a DELIVERED order"));
        assertTrue(all.contains("refused, cannot refund a REFUNDED order"));
        assertTrue(all.contains("PAID order: [SHIP, REFUND]"));
    }

    @Test
    void returnsAdded() {
        assertTrue(all.contains("DELIVERED order: [RETURN]"));
        assertTrue(all.contains("[PLACED, PAID, SHIPPED, DELIVERED, RETURNED, REFUNDED]"));
    }

    @Test
    void cells() {
        assertTrue(all.contains("7 statuses x 6 actions = 42 cells; 7 are allowed moves"));
    }
}
