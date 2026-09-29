package com.jk.explore.higherorder;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", HigherOrderDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("under 10: [Blue mug, Mini lamp, Tea towel]"));
        assertTrue(all.contains("filter(all, p -> p.price() < 10): [Blue mug, Mini lamp, Tea towel]"));
        assertTrue(all.contains(".and(inStock()): [Blue mug]"));
        assertTrue(all.contains("inStock().negate()):             [Travel mug]"));
        assertTrue(all.contains("20% off then 5 off: 31.00"));
        assertTrue(all.contains("5 off then 20% off: 32.00"));
    }
}
