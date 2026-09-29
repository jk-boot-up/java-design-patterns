package com.jk.explore.singletable;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", SingleTableDemo.run());
    }

    @Test
    void perType() {
        assertTrue(all.contains("[breakfast tea, desk lamp], 3 queries"));
    }

    @Test
    void single() {
        assertTrue(all.contains("[breakfast tea, desk lamp], 1 query"));
        assertTrue(all.contains("KETTLE-1 -> Electronics: 2-year warranty card"));
        assertTrue(all.contains("GIFT-1 -> GiftCard: activate £50 on dispatch"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("15 of 20 type-specific cells are empty"));
    }
}
