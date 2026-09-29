package com.jk.explore.offloadgateway;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/** The whole demo: real back-end services and a real Spring Cloud Gateway on local ports. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", GatewayOffloadingSpringDemo.run());
        assertTrue(all.contains("expired token -> orders:  200 orders for ana"), all);
        assertTrue(all.contains("expired token -> orders:  401 token expired"), all);
        assertTrue(all.contains("valid token -> orders:    200 orders for ana"), all);
        assertTrue(all.contains("8 requests in a row: 5 passed, 3 refused with 429"), all);
        assertTrue(all.contains("under a fifth of that with Content-Encoding gzip"), all);
        assertTrue(all.contains("spoofed X-Customer: ben -> 200 orders for ana"), all);
        assertTrue(all.contains("straight to the orders service, X-Customer: ben -> 200 orders for ben"), all);
    }
}
