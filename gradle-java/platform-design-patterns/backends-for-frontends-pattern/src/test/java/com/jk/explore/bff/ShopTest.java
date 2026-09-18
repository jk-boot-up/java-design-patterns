package com.jk.explore.bff;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ShopTest {

    private final CallLog log = new CallLog();
    private final Shop shop = new Shop(log);

    @Test
    @DisplayName("every service call is recorded as internal, never as a call from a device")
    void recordsItsCallsAsInternal() {
        shop.catalog("SKU-4417");
        shop.pricing("SKU-4417");

        assertEquals(2, log.countFrom(CallLog.Origin.INTERNAL));
        assertEquals(0, log.countFrom(CallLog.Origin.DEVICE));
        assertEquals(List.of("catalog", "pricing"), log.targetsFrom(CallLog.Origin.INTERNAL));
    }

    @Test
    @DisplayName("the same call twice returns the same bytes, so every printed number is stable")
    void isDeterministic() {
        assertEquals(shop.catalog("SKU-4417").bytes(), shop.catalog("SKU-4417").bytes());
        assertEquals(shop.reviews("SKU-4417").compact(), shop.reviews("SKU-4417").compact());
    }

    @Test
    @DisplayName("prices are whole pence, so formatting is somebody else's decision")
    void pricesArePence() {
        Doc pricing = shop.pricing("SKU-4417");

        assertEquals(5999, pricing.get("listPence"));
        assertEquals(4799, pricing.get("nowPence"));
    }

    @Test
    @DisplayName("the shop knows the higher price is too recent to advertise against")
    void knowsWhetherTheListPriceQualifies() {
        assertFalse((boolean) shop.pricing("SKU-4417").get("listPriceHeldLongEnough"));
    }

    @Test
    @DisplayName("the catalogue carries both a full-size image set and one thumbnail")
    void carriesBothImageSizes() {
        Doc catalog = shop.catalog("SKU-4417");

        assertEquals(5, ((List<?>) catalog.get("images")).size());
        assertTrue(catalog.get("thumbnail").toString().endsWith("hero-320.jpg"));
    }
}
