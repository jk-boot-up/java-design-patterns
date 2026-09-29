package com.jk.explore.specialcase;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", SpecialCaseDemo.run());

    @Test
    void nulls() {
        assertTrue(all.contains("Priya pays £38.00, added to newsletter"));
        assertTrue(all.contains("a guest checks out: NullPointerException"));
    }

    @Test
    void specialCases() {
        assertTrue(all.contains("Guest pays £40.00, points 0"));
        assertTrue(all.contains("Former customer pays £25.00, points 0"));
        assertTrue(all.contains("Unknown[formerId=C-99]"));
        assertTrue(all.contains("Guest: newsletter no"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("\"C-71\": Former customer"));
    }
}
