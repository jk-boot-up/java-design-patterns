package com.jk.explore.currying;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", CurryingDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("price(EU, STANDARD, 10.0) = 26.00"));
        assertTrue(all.contains("euStandard.apply(2.0) = 10.00"));
        assertTrue(all.contains("UK 5.00, EU 10.00, WORLD 20.00"));
        assertTrue(all.contains("EU express, with map: [14.00, 20.00, 52.00]"));
        assertTrue(all.contains("twentyOff.apply(45.0) = 36.00"));
        assertTrue(all.contains("applied to 45 it gives 11.00"));
    }
}
