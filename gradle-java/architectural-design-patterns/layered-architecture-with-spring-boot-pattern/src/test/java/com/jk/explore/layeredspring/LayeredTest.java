package com.jk.explore.layeredspring;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class LayeredTest {

    private static final String ONE_MACHINE = ShopApplication.ADA_ORDERS_ONE_MACHINE;

    @Test
    void aRealRequestGoesThroughAllFourLayers() {
        try (ShopApplication.Shop shop = new ShopApplication.Shop(false)) {
            String answer = shop.post("/orders", ONE_MACHINE);
            assertTrue(answer.startsWith("201"), answer);
            assertEquals(4, shop.products().stockOf("ESP-001"));
        }
    }

    @Test
    void aDeclinedCardRollsBackTheReservation() {
        try (ShopApplication.Shop shop = new ShopApplication.Shop(false)) {
            shop.cards().declineNextCharge();
            assertTrue(shop.post("/orders", ONE_MACHINE).startsWith("402"));
            assertEquals(5, shop.products().stockOf("ESP-001"));
        }
    }

    @Test
    void outOfStockBecomes422() {
        try (ShopApplication.Shop shop = new ShopApplication.Shop(false)) {
            assertTrue(shop.post("/orders", "{\"customer\":\"a\",\"sku\":\"ESP-001\",\"quantity\":10}").startsWith("422"));
        }
    }

    @Test
    void theShortcutRunsAndLeaksTheCostPrice() {
        try (ShopApplication.Shop shop = new ShopApplication.Shop(true)) {
            shop.post("/orders", ONE_MACHINE);
            String raw = shop.get("/raw-orders/ORD-000001");
            assertTrue(raw.startsWith("200"));
            assertTrue(raw.contains("costPence"));
        }
    }

    @Test
    void theLayeredResponseHidesTheCostPrice() {
        try (ShopApplication.Shop shop = new ShopApplication.Shop(false)) {
            assertFalse(shop.post("/orders", ONE_MACHINE).contains("costPence"));
        }
    }

    @Test
    void theShortcutIsNotScannedIntoTheNormalApplication() {
        try (ShopApplication.Shop shop = new ShopApplication.Shop(false)) {
            assertTrue(shop.get("/raw-orders/ORD-000001").startsWith("404"));
        }
    }

    @Test
    void theLayerRuleFindsOnlyTheShortcut() {
        var details = LayerRules.check().getFailureReport().getDetails();
        assertFalse(details.isEmpty());
        assertTrue(details.stream().allMatch(d -> d.contains("ShortcutController")));
    }
}
