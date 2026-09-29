package com.jk.explore.securegateway;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", SecureGatewayDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("X-Internal-Admin=true: 200 export of all 12000 orders"));
        assertTrue(all.contains("GET /orders/../admin/export:       200 export of all 12000 orders"));
        assertTrue(all.contains("holds the database password: true"));
        assertTrue(all.contains("X-Internal-Admin=true: 200 order 7"));
        assertTrue(all.contains("GET /orders/../admin/export: 404 not found (stopped at the gate)"));
        assertTrue(all.contains("DELETE /orders/7:            405"));
        assertTrue(all.contains("POST /orders:                201 order created"));
        assertTrue(all.contains("5 MB body: 413 too large"));
        assertTrue(all.contains("passed 3, refused 4"));
        assertTrue(all.contains("it holds credentials: false"));
    }
}
