package com.jk.explore.hedgedrequests;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", HedgedRequestsDemo.run());
        assertTrue(all.contains("median 20 ms, 99th percentile 1000 ms"));
        assertTrue(all.contains("99th percentile 70 ms, worst 70 ms"));
        assertTrue(all.contains("extra calls: 31 of 1000 (3%)"));
        assertTrue(all.contains("extra calls: 1000 of 1000 (100%)"));
        assertTrue(all.contains("from replica B"));
        assertTrue(all.contains("under 0.5 s"));
        assertTrue(all.contains("replica A's call cancelled: true"));
    }
}
