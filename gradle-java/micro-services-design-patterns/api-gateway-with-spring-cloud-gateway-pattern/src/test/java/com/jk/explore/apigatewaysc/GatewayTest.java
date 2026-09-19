package com.jk.explore.apigatewaysc;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class GatewayTest {

    @Test
    void oneAddressReachesEveryServiceWithThePrefixStrippedAndAHeaderAdded() {
        try (GatewayApplication.Shop shop = new GatewayApplication.Shop()) {
            assertEquals("200 pricing answers for /products/MUG-BLUE", shop.get("/api/pricing/products/MUG-BLUE", "t"));
            assertEquals("/products/MUG-BLUE", shop.pricing.lastPath());
            assertEquals("gateway", shop.pricing.lastSource());
            assertTrue(shop.get("/api/catalogue/x", "t").startsWith("200"));
            assertTrue(shop.get("/api/inventory/x", "t").startsWith("200"));
            assertTrue(shop.get("/api/recommendations/x", "t").startsWith("200"));
        }
    }

    @Test
    void aRequestWithoutATokenNeverReachesAnyService() {
        try (GatewayApplication.Shop shop = new GatewayApplication.Shop()) {
            assertEquals("401", shop.get("/api/catalogue/x", null));
            assertEquals("401", shop.get("/api/inventory/x", null));
            assertEquals(0, shop.total());
        }
    }

    @Test
    void aDeadServiceFailsOnlyItsOwnRoute() {
        try (GatewayApplication.Shop shop = new GatewayApplication.Shop()) {
            shop.recommendations.goDown();
            assertTrue(shop.get("/api/recommendations/x", "t").startsWith("500"));
            assertTrue(shop.get("/api/catalogue/x", "t").startsWith("200"));
        }
    }

    @Test
    void theGatewayForwardsOneRequestPerCallAndDoesNotMerge() {
        try (GatewayApplication.Shop shop = new GatewayApplication.Shop()) {
            shop.get("/api/catalogue/x", "t");
            shop.get("/api/pricing/x", "t");
            shop.get("/api/inventory/x", "t");
            assertEquals(3, shop.total());
        }
    }

    @Test
    void aSlowServiceIsAnsweredForWithA504() {
        try (GatewayApplication.Shop shop = new GatewayApplication.Shop()) {
            Gate stuck = new Gate(1);
            shop.pricing.slowDownAt(stuck);
            assertTrue(shop.get("/api/pricing/x", "t").startsWith("504"));
            stuck.open();
        }
    }
}
