package com.jk.explore.pollingconsumer;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", PollingConsumerDemo.run());

    @Test
    void push() {
        assertTrue(all.contains("printed: 10, refused: 40 (printer busy)"));
    }

    @Test
    void polling() {
        assertTrue(all.contains("printed: 50 of 50 in 10 ticks (1.0 s); refused: 0"));
        assertTrue(all.contains("printed 5, waiting safely in the queue: 15"));
        assertTrue(all.contains("printed 20 of 20, none lost"));
        assertTrue(all.contains("600 polls, 600 empty"));
    }
}
