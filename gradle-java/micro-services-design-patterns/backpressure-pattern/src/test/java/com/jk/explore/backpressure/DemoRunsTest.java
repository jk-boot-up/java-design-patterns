package com.jk.explore.backpressure;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", BackpressureDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("after 10 s: 1000 indexed, 9000 waiting in memory"));
        assertTrue(all.contains("never more than 500 waiting; all 10000 indexed in 100 s"));
        assertTrue(all.contains("indexed 10000; at most 10 products were ever in flight"));
        assertTrue(all.contains("10 delivered, the latest for each"));
        assertTrue(all.contains("SKU-3 now: 7"));
    }
}
