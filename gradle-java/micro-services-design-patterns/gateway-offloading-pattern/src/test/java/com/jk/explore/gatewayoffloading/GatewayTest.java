package com.jk.explore.gatewayoffloading;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class GatewayTest {

    private final ShopService cart = new ShopService("cart", "");
    private final Gateway gateway = new Gateway(100, 2).route("/cart", cart);

    @Test
    void missingTokenNeverReachesTheService() {
        assertEquals(401, gateway.handle(Request.of("/cart")).status());
        assertEquals(0, cart.calls());
    }

    @Test
    void customerIsPassedOn() {
        Response r = gateway.handle(Request.of("/cart", "Authorization", Tokens.issue("zoe", 200)));
        assertEquals("cart for zoe", r.text());
    }

    @Test
    void limitResetsEachSecond() {
        String t = Tokens.issue("zoe", 200);
        gateway.handle(Request.of("/cart", "Authorization", t));
        gateway.handle(Request.of("/cart", "Authorization", t));
        assertEquals(429, gateway.handle(Request.of("/cart", "Authorization", t)).status());
        gateway.tick(101);
        assertEquals(200, gateway.handle(Request.of("/cart", "Authorization", t)).status());
    }

    @Test
    void unknownPathIs404() {
        assertEquals(404, gateway.handle(Request.of("/nope", "Authorization", Tokens.issue("zoe", 200))).status());
        assertTrue(cart.calls() == 0);
    }
}
