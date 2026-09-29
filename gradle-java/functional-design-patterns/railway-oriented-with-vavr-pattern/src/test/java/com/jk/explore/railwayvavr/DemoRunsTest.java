package com.jk.explore.railwayvavr;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", VavrRailwayDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("LegacyPayments.charge threw \"card declined\""), all);
        assertTrue(all.contains("2 mugs, good card: 200 order ORD-1 confirmed"), all);
        assertTrue(all.contains("ran: validate; skipped: reserve, charge, email"), all);
        assertTrue(all.contains("card declined: 422 card declined (at charge)"), all);
        assertTrue(all.contains("total 23.98"), all);
        assertTrue(all.contains("with orElse: back-order placed"), all);
        assertTrue(all.contains("Either chain: 422 the cart is empty (at validate)"), all);
        assertTrue(all.contains("Validation.combine: the cart is empty and no card given"), all);
    }
}
