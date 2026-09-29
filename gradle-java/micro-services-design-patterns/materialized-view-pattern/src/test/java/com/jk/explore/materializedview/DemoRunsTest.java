package com.jk.explore.materializedview;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", MaterializedViewDemo.run());

    @Test
    void queryOnReadCosts() {
        assertTrue(all.contains("7 service calls, about 280 ms"));
        assertTrue(all.contains("the page fails, catalogue service unavailable"));
    }

    @Test
    void viewServesWithoutCalls() {
        assertTrue(all.contains("3 rows, 0 service calls, catalogue still down"));
        assertTrue(all.contains("same page as before: true"));
    }

    @Test
    void lagThenCatchUp() {
        assertTrue(all.contains("page right now: ORD-3 1 x kettle (placed)"));
        assertTrue(all.contains("a moment later: ORD-3 1 x kettle (shipped)"));
    }

    @Test
    void rebuildMatches() {
        assertTrue(all.contains("replayed 8 events"));
        assertTrue(all.contains("rebuilt page equals the old one: true"));
    }

    @Test
    void renameRewritesTwoRows() {
        assertTrue(all.contains("the view rewrote 2 rows"));
    }
}
