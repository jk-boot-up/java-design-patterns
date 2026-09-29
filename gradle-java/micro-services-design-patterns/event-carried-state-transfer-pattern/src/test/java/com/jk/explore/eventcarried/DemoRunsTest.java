package com.jk.explore.eventcarried;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", EventCarriedDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("100 labels: 100 printed, 100 calls to the customer service"));
        assertTrue(all.contains("customer service down: 0 of 100 labels printed"));
        assertTrue(all.contains("100 labels: 100 printed, 0 calls to the customer service"));
        assertTrue(all.contains("customer service down: 100 of 100 labels still printed"));
        assertTrue(all.contains("label printed now:  ORD-1 -> 1 High Street, Leeds"));
        assertTrue(all.contains("after the event:    ORD-1 -> 9 Mill Lane, York"));
        assertTrue(all.contains("without versions: ORD-2 -> 1 Park Road, Hull"));
        assertTrue(all.contains("with versions:    ORD-2 -> 4 Quay Street, Bristol  (version 2 ignored after 3)"));
    }
}
