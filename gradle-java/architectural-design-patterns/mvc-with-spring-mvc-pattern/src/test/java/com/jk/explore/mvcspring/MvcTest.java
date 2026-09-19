package com.jk.explore.mvcspring;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class MvcTest {

    @Test
    void theModelAppliesTheDiscountWithoutAServer() {
        OrderSummary s = OrderSummary.of(new OrderStore().find("ORD-000001").orElseThrow());
        assertEquals(32500, s.subtotalPence());
        assertEquals(3250, s.discountPence());
        assertEquals(29250, s.totalPence());
    }

    @Test
    void noDiscountUnderThreeHundredPounds() {
        var order = new OrderStore().place("bo", "BNS-220", 1);
        assertEquals(0, OrderSummary.of(order).discountPence());
    }

    @Test
    void htmlAndJsonViewsShowTheSameTotal() {
        try (SummaryApplication.Shop shop = new SummaryApplication.Shop()) {
            var html = shop.get("/orders/ORD-000001", "text/html");
            var json = shop.get("/orders/ORD-000001", "application/json");
            assertTrue(html.headers().firstValue("Content-Type").orElse("").startsWith("text/html"));
            assertTrue(html.body().contains("£292.50"));
            assertTrue(json.body().contains("\"totalPence\":29250"));
        }
    }

    @Test
    void oneSummaryIsComputedPerPageView() {
        try (SummaryApplication.Shop shop = new SummaryApplication.Shop()) {
            int before = OrderSummary.COMPUTATIONS.get();
            shop.get("/orders/ORD-000001", "text/html");
            assertEquals(1, OrderSummary.COMPUTATIONS.get() - before);
        }
    }

    @Test
    void aSumInTheViewIgnoresTheDiscountAndBreaksOnOneLine() {
        try (SummaryApplication.Shop shop = new SummaryApplication.Shop()) {
            assertTrue(shop.get("/orders/ORD-000001/naive", "text/html").body().contains("32500"));
            shop.postForm("/orders", "customer=bo&sku=BNS-220&quantity=1");
            assertEquals(500, shop.get("/orders/ORD-000002/naive", "text/html").statusCode());
            assertEquals(200, shop.get("/orders/ORD-000002", "text/html").statusCode());
        }
    }

    @Test
    void aPostAnswersWithARedirect() {
        try (SummaryApplication.Shop shop = new SummaryApplication.Shop()) {
            var r = shop.postForm("/orders", "customer=bo&sku=BNS-220&quantity=1");
            assertTrue(r.statusCode() == 302 || r.statusCode() == 303);
            assertTrue(r.headers().firstValue("Location").orElse("").endsWith("/orders/ORD-000002"));
        }
    }
}
