package com.jk.explore.resequencercamel;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", CamelResequencerDemo.run());
        assertTrue(all.contains("the customer saw: [PLACED, PACKED, PAID, DELIVERED, SHIPPED]"));
        assertTrue(all.contains("the customer saw: [PLACED, PAID, PACKED, SHIPPED, DELIVERED]"));
        assertTrue(all.contains("the first update appeared only after about 0.3 s"));
        assertTrue(all.contains("after 4 arrivals the customer sees: []"));
        assertTrue(all.contains("after the 5th: [PLACED, PAID, PACKED, SHIPPED, DELIVERED]"));
        assertTrue(all.contains("released: [ORD-2 PLACED, ORD-2 PAID, ORD-3 PLACED, ORD-3 PAID, ORD-3 PACKED]"));
        assertTrue(all.contains("the page still says PAID while they wait for #3"));
        assertTrue(all.contains("after about half a second the gap is given up: the page says DELIVERED"));
    }
}
