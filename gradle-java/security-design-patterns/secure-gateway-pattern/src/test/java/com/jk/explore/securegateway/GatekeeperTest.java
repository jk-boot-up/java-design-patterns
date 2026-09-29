package com.jk.explore.securegateway;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Map;
import org.junit.jupiter.api.Test;

class GatekeeperTest {

    private final Gatekeeper gate = new Gatekeeper(new OrderService("pw"));

    @Test
    void unknownPathNeverReachesTheService() {
        assertTrue(gate.handle(HttpRequest.get("/admin/export")).startsWith("404"));
        assertEquals(0, gate.passed());
    }

    @Test
    void longIdIsRefused() {
        assertTrue(gate.handle(HttpRequest.get("/orders/1234567890")).startsWith("404"));
    }

    @Test
    void bodyAtTheLimitPasses() {
        assertEquals("201 order created",
                gate.handle(new HttpRequest("POST", "/orders", Map.of(), Gatekeeper.MAX_BODY)));
    }
}
