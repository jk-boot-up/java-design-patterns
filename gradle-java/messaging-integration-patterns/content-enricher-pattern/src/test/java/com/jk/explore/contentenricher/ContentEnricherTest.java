package com.jk.explore.contentenricher;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

class ContentEnricherTest {

    private final OrderPlaced order = new OrderPlaced("ORD-1", "C-17", List.of("kettle"));

    @Test
    void addsNameAddressAndTier() {
        EnrichedOrder e = new ContentEnricher(ContentEnricherDemo.directory(), false).enrich(order).orElseThrow();
        assertEquals("Priya Shah", e.name());
        assertEquals("4 Mill Lane, Leeds", e.address());
        assertEquals("GOLD", e.tier());
        assertEquals(List.of("kettle"), e.items());
    }

    @Test
    void cacheLooksEachCustomerUpOnce() {
        CustomerDirectory d = ContentEnricherDemo.directory();
        ContentEnricher e = new ContentEnricher(d, true);
        ContentEnricherDemo.orders().forEach(e::enrich);
        assertEquals(2, d.lookups());
    }

    @Test
    void withoutCacheEveryOrderIsLookedUp() {
        CustomerDirectory d = ContentEnricherDemo.directory();
        ContentEnricher e = new ContentEnricher(d, false);
        ContentEnricherDemo.orders().forEach(e::enrich);
        assertEquals(3, d.lookups());
    }

    @Test
    void unknownCustomerGoesToProblemList() {
        ContentEnricher e = new ContentEnricher(ContentEnricherDemo.directory(), true);
        assertFalse(e.enrich(new OrderPlaced("ORD-4", "C-99", List.of())).isPresent());
        assertEquals(List.of("ORD-4: no customer C-99"), e.problems());
    }

    @Test
    void enrichedReceiversNeedNoCustomerService() {
        CustomerDirectory d = ContentEnricherDemo.directory();
        EnrichedOrder e = new ContentEnricher(d, false).enrich(order).orElseThrow();
        d.setUp(false);
        assertEquals("pack ORD-1 for 4 Mill Lane, Leeds", Receivers.pack(e));
        assertThrows(IllegalStateException.class, () -> Receivers.packThin(order, d));
    }

    @Test
    void enrichedCopyDoesNotFollowLaterChanges() {
        CustomerDirectory d = ContentEnricherDemo.directory();
        EnrichedOrder e = new ContentEnricher(d, false).enrich(order).orElseThrow();
        d.moveHouse("C-17", "12 High Street, York");
        assertEquals("4 Mill Lane, Leeds", e.address());
    }

    @Test
    void enrichedMessageIsBigger() {
        EnrichedOrder e = new ContentEnricher(ContentEnricherDemo.directory(), false).enrich(order).orElseThrow();
        assertTrue(e.size() > order.size());
    }
}
