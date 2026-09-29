package com.jk.explore.gatewayoffloading;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", GatewayOffloadingDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("expired token -> orders: 200 orders for ana"));
        assertTrue(all.contains("expired token -> orders: 401 token expired"));
        assertTrue(all.contains("valid token -> orders: 200 orders for ana"));
        assertTrue(all.contains("8 requests in one second: 5 passed, 3 refused with 429"));
        assertTrue(all.contains("the orders service saw 5"));
        assertTrue(all.contains("10094 bytes plain, under a fifth of that gzipped"));
        assertTrue(all.contains("claiming to be ben: 200 orders for ben"));
    }
}
