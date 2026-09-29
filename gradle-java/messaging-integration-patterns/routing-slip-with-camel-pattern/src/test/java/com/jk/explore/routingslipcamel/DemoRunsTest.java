package com.jk.explore.routingslipcamel;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", CamelRoutingSlipDemo.run());
        assertTrue(all.contains("4 orders x 6 steps = 24 visits; 15 did any work"));
        assertTrue(all.contains("ORD-3 slip: [validate, age-check, charge, pack]"));
        assertTrue(all.contains("15 visits in all, 15 doing work"));
        assertTrue(all.contains("ORD-2 went: [validate, charge, gift-wrap, pack]"));
        assertTrue(all.contains("ORD-4 now went: [validate, customs, fraud-check, charge, pack]"));
        assertTrue(all.contains("went [validate, age-check]; still on the slip: [charge, pack]"));
        assertTrue(all.contains("ORD-5 went [validate, age-check, notify-customer]"));
    }
}
