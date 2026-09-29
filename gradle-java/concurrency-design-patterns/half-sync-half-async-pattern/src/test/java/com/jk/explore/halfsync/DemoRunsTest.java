package com.jk.explore.halfsync;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", HalfSyncHalfAsyncDemo.run());
    }

    @Test
    void eventThreadOnly() {
        assertTrue(all.contains("the last order waited over 1.5 s just to be accepted"));
    }

    @Test
    void halfSyncHalfAsync() {
        assertTrue(all.contains("every order accepted within 0.1 s"));
        assertTrue(all.contains("all 20 orders done in under 1 s"));
        assertTrue(all.contains("the queue held 10 or more orders"));
    }

    @Test
    void fullQueue() {
        assertTrue(all.contains("queue of 10: 10 of 20 orders turned away"));
    }
}
