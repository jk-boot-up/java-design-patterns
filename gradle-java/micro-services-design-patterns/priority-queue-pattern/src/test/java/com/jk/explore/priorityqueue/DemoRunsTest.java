package com.jk.explore.priorityqueue;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", PriorityQueueDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("picked at 9:10, after the van has gone"));
        assertTrue(all.contains("all 5 same-day orders picked by 9:01"));
        assertTrue(all.contains("1000 standard orders ahead of them: same-day still picked by 9:01"));
        assertTrue(all.contains("standard orders picked in 10 minutes: 0 of 20"));
        assertTrue(all.contains("oldest standard orders: 20 of 20 picked"));
    }
}
