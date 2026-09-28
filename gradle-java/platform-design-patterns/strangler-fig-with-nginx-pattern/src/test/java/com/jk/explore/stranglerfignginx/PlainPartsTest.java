package com.jk.explore.stranglerfignginx;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.concurrent.CompletableFuture;
import org.junit.jupiter.api.Test;

/**
 * The parts that need no container: the configuration text the demo writes, and the two shop
 * services, called directly on this machine without NGINX in front.
 */
class PlainPartsTest {

    @Test
    void everyRouteStartsOnTheOldShopThroughOneCatchAllRule() {
        String conf = NginxConfig.everythingOnTheOldShop().render(1, 1111, 2222);
        assertTrue(conf.contains("upstream old_shop    { server host.testcontainers.internal:1111; }"), conf);
        assertTrue(conf.contains("upstream new_service { server host.testcontainers.internal:2222; }"), conf);
        assertTrue(conf.contains("location / {\n            proxy_pass http://old_shop;"), conf);
        assertTrue(conf.contains("location = /router/generation { return 200 \"1\"; }"), conf);
        assertTrue(conf.contains("worker_processes 1;"), conf);
        assertFalse(conf.contains("new_service;"), conf);
    }

    @Test
    void theBigBangSendsTheCatchAllToTheNewService() {
        String conf = NginxConfig.bigBang().render(2, 1111, 2222);
        assertTrue(conf.contains("location / {\n            proxy_pass http://new_service;"), conf);
    }

    @Test
    void movingARouteAddsOneLocationAndChangesNothingElse() {
        String before = NginxConfig.everythingOnTheOldShop().render(3, 1111, 2222);
        String after = NginxConfig.everythingOnTheOldShop().move("/api/prices/").render(3, 1111, 2222);
        String added = "        location /api/prices/ {\n            proxy_pass http://new_service;\n        }\n";
        assertEquals(before, after.replace(added, ""));
    }

    @Test
    void theThreeWaysOfWritingAMoveDifferByOneCharacterEach() {
        assertEquals("location /api/prices/", NginxConfig.everythingOnTheOldShop().move("/api/prices/").moves().get(0).locationLine());
        assertEquals("location ^~ /api/prices/", NginxConfig.everythingOnTheOldShop().moveAndStopLooking("/api/prices/").moves().get(0).locationLine());
        assertEquals("proxy_pass http://new_service;", NginxConfig.everythingOnTheOldShop().moveAndStopLooking("/api/prices/").moves().get(0).proxyPassLine());
        assertEquals("proxy_pass http://new_service/;", NginxConfig.everythingOnTheOldShop().moveWithTrailingSlash("/api/prices/").moves().get(0).proxyPassLine());
    }

    @Test
    void theOldCachingRuleIsARegularExpressionWrittenBeforeAnyMove() {
        String conf = NginxConfig.everythingOnTheOldShop().withLegacyCacheRule().move("/api/prices/").render(4, 1111, 2222);
        assertTrue(conf.contains("location ~ ^/api/(prices|stock)/ {"), conf);
        assertTrue(conf.indexOf("location ~ ^/api/(prices|stock)/") < conf.indexOf("location /api/prices/"), conf);
    }

    @Test
    void theOldShopKeepsTheBasketUnderItsOwnCookieAndChecksItOut() {
        try (OldShop old = OldShop.start()) {
            Browser customer = new Browser("http://localhost:" + old.port());
            customer.post("/api/basket/items?sku=SKU-1");
            customer.post("/api/basket/items?sku=SKU-2");
            assertEquals("basket: 3 items", customer.post("/api/basket/items?sku=SKU-3").body());
            assertEquals("L-1", customer.cookies().get(OldShop.SESSION_COOKIE));
            Answer order = customer.post("/api/checkout");
            assertEquals(200, order.status());
            assertEquals("order 1002 placed: 3 items, 4249 pence", order.body());
            assertEquals(OldShop.NAME, order.servedBy());
        }
    }

    @Test
    void theNewServiceIgnoresTheOldShopsCookie() {
        try (NewService fresh = NewService.start()) {
            Browser customer = new Browser("http://localhost:" + fresh.port()).withCookie(OldShop.SESSION_COOKIE, "L-1");
            Answer answer = customer.post("/api/checkout");
            assertEquals(422, answer.status());
            assertEquals("your basket is empty", answer.body());
            assertEquals("LEGACYSESSION=L-1", fresh.lastCookieReceived());
            assertEquals(404, customer.get("/api/stock/SKU-1").status());
        }
    }

    @Test
    void theNewServiceWritesDownEveryPathItReceives() {
        try (NewService fresh = NewService.start()) {
            Browser direct = new Browser("http://localhost:" + fresh.port());
            assertEquals(200, direct.get("/api/prices/SKU-1").status());
            assertEquals(404, direct.get("/SKU-1").status());
            assertEquals("/SKU-1", fresh.lastPathReceived());
        }
    }

    @Test
    void theNewServiceCanGoDownAndComeBackOnTheSamePort() {
        try (NewService fresh = NewService.start()) {
            Browser direct = new Browser("http://localhost:" + fresh.port());
            fresh.stop();
            assertThrows(IllegalStateException.class, () -> direct.get("/api/prices/SKU-1"));
            fresh.startAgain();
            assertEquals(200, direct.get("/api/prices/SKU-1").status());
        }
    }

    @Test
    void aHeldPriceRequestStaysOpenUntilItIsReleased() {
        try (OldShop old = OldShop.start()) {
            old.holdTheNextPriceRequest();
            Browser customer = new Browser("http://localhost:" + old.port());
            CompletableFuture<Answer> open = CompletableFuture.supplyAsync(() -> customer.get("/api/prices/SKU-1"));
            Poll.until("the held request to arrive", old::heldRequestArrived);
            assertFalse(open.isDone());
            old.releaseHeldRequest();
            assertEquals("SKU-1 costs 1299 pence", open.join().body());
        }
    }
}
