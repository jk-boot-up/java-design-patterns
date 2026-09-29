package com.jk.explore.routingslip;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", RoutingSlipDemo.run());

    @Test
    void fixed() {
        assertTrue(all.contains("4 orders x 6 steps = 24 visits; 15 did any work"));
    }

    @Test
    void slips() {
        assertTrue(all.contains("ORD-2 slip: [validate, charge, gift-wrap, pack]"));
        assertTrue(all.contains("ORD-4 slip: [validate, customs, charge, pack]"));
        assertTrue(all.contains("15 visits in all"));
        assertTrue(all.contains("ORD-4 slip: [validate, customs, fraud-check, charge, pack]"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("stopped at age-check; still on the slip: [charge, pack]"));
    }
}
