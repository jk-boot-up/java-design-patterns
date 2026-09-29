package com.jk.explore.proactor;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", ProactorDemo.run());
    }

    @Test
    void blocking() {
        assertTrue(all.contains("5 prices in over 0.9 s"));
    }

    @Test
    void proactor() {
        assertTrue(all.contains("start() returned, in under 0.1 s"));
        assertTrue(all.contains("all 5 answers in under 0.6 s"));
        assertTrue(all.contains("cheapest: £18.90"));
    }

    @Test
    void failure() {
        assertTrue(all.contains("its failed() handler ran: true"));
        assertTrue(all.contains("the other 2 answered as normal"));
    }
}
