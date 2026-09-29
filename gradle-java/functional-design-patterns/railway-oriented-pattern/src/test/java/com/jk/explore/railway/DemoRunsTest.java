package com.jk.explore.railway;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", RailwayDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("out of stock:  409 LAMP is out of stock"));
        assertTrue(all.contains("card declined: 500 internal server error"));
        assertTrue(all.contains("2 mugs, good card: 200 order ORD-1 confirmed"));
        assertTrue(all.contains("ran: validate, reserve, charge, email"));
        assertTrue(all.contains("ran: validate; skipped: reserve, charge, email"));
        assertTrue(all.contains("422 card declined (at charge)"));
        assertTrue(all.contains("ran: validate, reserve, charge; skipped: email"));
        assertTrue(all.contains("with map: total 23.98"));
        assertTrue(all.contains("recovered: back-order placed"));
        assertTrue(all.contains("empty cart and no card: 422 the cart is empty (at validate)"));
    }
}
