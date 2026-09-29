package com.jk.explore.scheduler;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", SchedulerDemo.run());
    }

    @Test
    void orders() {
        assertTrue(all.contains("printed: [STD-1, STD-2, STD-3, EXP-1, EXP-2, EXP-3]"));
        assertTrue(all.contains("printed: [EXP-1, EXP-2, EXP-3, STD-1, STD-2, STD-3]"));
        assertTrue(all.contains("printed: [STD-2, EXP-2, STD-3, EXP-3, EXP-1, STD-1]"));
        assertTrue(all.contains("rush of express: [EXP-1, EXP-2, EXP-3, EXP-4, EXP-5, STD-1]"));
        assertTrue(all.contains("3 times:    [EXP-1, EXP-2, EXP-3, STD-1, EXP-4, EXP-5]"));
    }
}
