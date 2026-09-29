package com.jk.explore.leaderfollowers;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", LeaderFollowersDemo.run());
    }

    @Test
    void dispatcher() {
        assertTrue(all.contains("hand-offs between threads: 20; handled by the thread that received it: 0"));
    }

    @Test
    void leaderFollowers() {
        assertTrue(all.contains("waiting for a message at the same moment: 1"));
        assertTrue(all.contains("leadership passed on 20 times"));
        assertTrue(all.contains("20 of 20; hand-offs between threads: 0"));
    }

    @Test
    void orderNotKept() {
        assertTrue(all.contains("finished in the order: [ORD-1 cancel order, ORD-1 place order]"));
    }
}
