package com.jk.explore.wiretap;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", WireTapDemo.run());
    }

    @Test
    void handLogging() {
        assertTrue(all.contains("messages sent: 4; messages in the log: 3"));
        assertTrue(all.contains("card 4929123412341234"));
    }

    @Test
    void tap() {
        assertTrue(all.contains("audit: REFUND ORD-1 £30.00 card **** 1234"));
        assertTrue(all.contains("4 of 4 copied"));
        assertTrue(all.contains("audit still has 4 lines"));
        assertTrue(all.contains("net takings seen by the meter: £58.42"));
    }

    @Test
    void slowTap() {
        assertTrue(all.contains("4 payments took over 0.4 s"));
        assertTrue(all.contains("the same tap on its own thread: under 0.05 s"));
    }
}
