package com.jk.explore.broker;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", BrokerDemo.run());
    }

    @Test
    void hardCodedBreaks() {
        assertTrue(all.contains("still using the old address: FAILED"));
    }

    @Test
    void brokerWorks() {
        assertTrue(all.contains("/call/stock?sku=KETTLE-1 -> 4"));
        assertTrue(all.contains("checkout, unchanged: /call/stock?sku=MUG-1 -> 20"));
        assertTrue(all.contains("call 1: £30.00 (from price-a)"));
        assertTrue(all.contains("call 2: £30.00 (from price-b)"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("= 2 network requests"));
        assertTrue(all.contains("the broker stops: FAILED"));
    }
}
