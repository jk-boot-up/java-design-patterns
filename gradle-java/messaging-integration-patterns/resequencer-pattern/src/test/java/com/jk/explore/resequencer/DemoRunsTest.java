package com.jk.explore.resequencer;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", ResequencerDemo.run());

    @Test
    void asArrived() {
        assertTrue(all.contains("the customer saw: [PLACED, PACKED, PAID, DELIVERED, SHIPPED]"));
        assertTrue(all.contains("final status: SHIPPED, but the parcel was DELIVERED"));
    }

    @Test
    void resequenced() {
        assertTrue(all.contains("the customer saw: [PLACED, PAID, PACKED, SHIPPED, DELIVERED]"));
        assertTrue(all.contains("received ORD-1#3 PACKED; holding [3]"));
        assertTrue(all.contains("[ORD-3 PLACED, ORD-2 PLACED, ORD-2 PAID, ORD-3 PAID, ORD-3 PACKED]"));
    }

    @Test
    void lostMessage() {
        assertTrue(all.contains("page still says PAID, holding 1"));
        assertTrue(all.contains("the gap is given up on: page says DELIVERED"));
    }
}
