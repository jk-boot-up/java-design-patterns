package com.jk.explore.contextmap;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", ContextMapDemo.run());

    @Test
    void separate() {
        assertTrue(all.contains("shipping label after the converter: 4 Mill Lane, Leeds"));
    }

    @Test
    void kernel() {
        assertTrue(all.contains("sales: ORD-1 for £38.00"));
        assertTrue(all.contains("shipping: PARCEL-1 to Flat 2, 4 Mill Lane, Leeds, insured for £38.00"));
    }

    @Test
    void map() {
        assertTrue(all.contains("catalog -> sales: customer/supplier"));
        assertTrue(all.contains("imports the map does not allow: 0"));
        assertTrue(all.contains("check: shipping/Shipping.java imports sales, which the map does not allow"));
    }
}
