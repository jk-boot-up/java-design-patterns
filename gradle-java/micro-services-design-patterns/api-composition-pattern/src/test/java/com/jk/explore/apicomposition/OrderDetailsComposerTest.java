package com.jk.explore.apicomposition;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** The composed page: what it costs, and what it does when a service is missing. */
class OrderDetailsComposerTest {

    private static final String ORDER_ID = "ord-3001";

    private SimulatedClock clock;
    private CallLog log;
    private OrderService orders;
    private CatalogService catalog;
    private ShippingService shipping;
    private OrderDetailsComposer composer;

    @BeforeEach
    void setUp() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
        orders = new OrderService(clock, log);
        catalog = new CatalogService(clock, log);
        shipping = new ShippingService(clock, log);
        composer = new OrderDetailsComposer(orders, catalog, shipping, clock, log);
    }

    @Test
    @DisplayName("the page has the order, the names and the delivery status on it")
    void itAssemblesTheWholePage() {
        OrderDetailsPage page = composer.pageFor(ORDER_ID);

        assertEquals(ORDER_ID, page.orderId());
        assertEquals(2, page.lines().size());
        assertEquals("Stainless Steel Kettle", page.lines().get(0).productName());
        assertEquals(Money.pence(3499 + 4 * 899), page.total());
        assertEquals("Royal Mail", page.delivery().carrier());
        assertTrue(page.isComplete());
    }

    @Test
    @DisplayName("the two independent calls cost the slower of them, not both")
    void itPaysForTheSlowestBranchOnly() {
        composer.pageFor(ORDER_ID);

        long sequentialCost = OrderService.LATENCY_MILLIS + CatalogService.LATENCY_MILLIS
                + ShippingService.LATENCY_MILLIS;
        long composedCost = OrderService.LATENCY_MILLIS
                + Math.max(CatalogService.LATENCY_MILLIS, ShippingService.LATENCY_MILLIS);

        assertEquals(composedCost, log.elapsedMillis());
        assertTrue(log.elapsedMillis() < sequentialCost);
    }

    @Test
    @DisplayName("the page is only ever as fast as its slowest dependency")
    void theSlowestDependencySetsThePace() {
        ShippingService slow = new ShippingService(clock, log, 400);

        new OrderDetailsComposer(orders, catalog, slow, clock, log).pageFor(ORDER_ID);

        assertEquals(OrderService.LATENCY_MILLIS + 400, log.elapsedMillis());
    }

    @Test
    @DisplayName("each service is asked exactly once, however many lines the order has")
    void itAsksEachServiceOnce() {
        composer.pageFor(ORDER_ID);

        assertEquals(1, orders.callsReceived());
        assertEquals(1, catalog.callsReceived());
        assertEquals(1, shipping.callsReceived());
    }

    @Test
    @DisplayName("an optional service failing costs a section, not the page")
    void itReturnsAPartialPageWhenShippingIsDown() {
        shipping.goDown(1);

        OrderDetailsPage page = composer.pageFor(ORDER_ID);

        assertFalse(page.isComplete());
        assertEquals(List.of("delivery status"), page.missingSections());
        assertEquals(2, page.lines().size());
        assertEquals(Money.pence(3499 + 4 * 899), page.total());
        assertFalse(page.delivery().isKnown());
    }

    @Test
    @DisplayName("a missing delivery status says so rather than guessing")
    void itDoesNotInventADeliveryStatus() {
        shipping.goDown(1);

        DeliveryStatus delivery = composer.pageFor(ORDER_ID).delivery();

        assertTrue(delivery.state().contains("cannot check"), delivery.state());
    }

    @Test
    @DisplayName("a missing catalog leaves the sku codes visible and the money right")
    void itFallsBackToSkuCodesWhenCatalogIsDown() {
        catalog.goDown(1);

        OrderDetailsPage page = composer.pageFor(ORDER_ID);

        assertEquals(List.of("product names"), page.missingSections());
        assertEquals(CatalogService.NAME_UNAVAILABLE, page.lines().get(0).productName());
        assertEquals("SKU-KETTLE", page.lines().get(0).sku());
        assertEquals(Money.pence(3499 + 4 * 899), page.total());
    }

    @Test
    @DisplayName("both optional services down still leaves a page worth showing")
    void itSurvivesTwoOptionalFailures() {
        catalog.goDown(1);
        shipping.goDown(1);

        OrderDetailsPage page = composer.pageFor(ORDER_ID);

        assertEquals(List.of("product names", "delivery status"), page.missingSections());
        assertEquals(Money.pence(3499 + 4 * 899), page.total());
    }

    @Test
    @DisplayName("the required service failing means no page")
    void itRefusesToBuildAPageWithoutTheOrder() {
        orders.goDown(1);

        assertThrows(ServiceUnavailableException.class, () -> composer.pageFor(ORDER_ID));
    }

    @Test
    @DisplayName("nothing else is called once the required service has failed")
    void itStopsWhenTheOrderIsMissing() {
        orders.goDown(1);

        assertThrows(ServiceUnavailableException.class, () -> composer.pageFor(ORDER_ID));
        assertEquals(0, catalog.callsReceived());
        assertEquals(0, shipping.callsReceived());
    }

    @Test
    @DisplayName("a failed branch is written into the timeline, not hidden")
    void itLogsThePartialPage() {
        shipping.goDown(1);

        composer.pageFor(ORDER_ID);

        assertTrue(log.timeline().contains("FAILED"), log.timeline());
        assertTrue(log.timeline().contains("PARTIAL"), log.timeline());
        assertTrue(log.timeline().contains("1 failed"), log.timeline());
    }

    @Test
    @DisplayName("the parallel branches both start at the same moment")
    void bothBranchesLeaveTogether() {
        composer.pageFor(ORDER_ID);

        List<CallLog.Entry> parallel = log.entries().stream()
                .filter(e -> e.service().equals("Catalog") || e.service().equals("Shipping"))
                .toList();

        assertEquals(2, parallel.size());
        assertEquals(parallel.get(0).startedAt(), parallel.get(1).startedAt());
    }
}
