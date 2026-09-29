package com.jk.explore.backpressurereactor;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", ReactorBackpressureDemo.run());
        assertTrue(all.contains("Reactor stops the stream: OverflowException"), all);
        assertTrue(all.contains("indexed before it failed: only part of the 10000"), all);
        assertTrue(all.contains("indexed 10000, never more than 10 asked for"), all);
        assertTrue(all.contains("requests of [10, 8, 8, 8] ... for 100 products"), all);
        assertTrue(all.contains("the shop asked twice and got [1000, 1]"), all);
    }
}
