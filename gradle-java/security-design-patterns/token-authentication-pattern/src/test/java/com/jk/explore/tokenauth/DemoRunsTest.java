package com.jk.explore.tokenauth;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", TokenAuthDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("routed to B: 401 please sign in"));
        assertTrue(all.contains("token payload: {\"sub\":\"ana\",\"exp\":1000900,\"jti\":\"t1\"}"));
        assertTrue(all.contains("server B: 200 ana's cart  (no shared session store)"));
        assertTrue(all.contains("payload changed to ben: 401 bad signature"));
        assertTrue(all.contains("used after 15 minutes:  401 expired"));
        assertTrue(all.contains("the token alone still says: 200 ana's cart"));
        assertTrue(all.contains("with a revoked list, server A: 401 revoked"));
        assertTrue(all.contains("but server B has its own list: 200 ana's cart"));
    }
}
