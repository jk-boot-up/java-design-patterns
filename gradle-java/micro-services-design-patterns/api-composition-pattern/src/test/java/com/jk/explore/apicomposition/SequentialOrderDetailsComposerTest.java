package com.jk.explore.apicomposition;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The sequential composer, and every test in here passes.
 *
 * That is the point of the class. The code is correct, the page is right, and a code
 * review would wave it through. Its cost is a number in a timeline and a behaviour during
 * an outage, and neither of those is something "did it throw" can see. So the cost is
 * written down as assertions instead.
 */
class SequentialOrderDetailsComposerTest {

    private static final String ORDER_ID = "ord-3001";

    private CallLog log;
    private OrderService orders;
    private CatalogService catalog;
    private ShippingService shipping;
    private SequentialOrderDetailsComposer composer;

    @BeforeEach
    void setUp() {
        SimulatedClock clock = new SimulatedClock();
        log = new CallLog(clock);
        orders = new OrderService(clock, log);
        catalog = new CatalogService(clock, log);
        shipping = new ShippingService(clock, log);
        composer = new SequentialOrderDetailsComposer(orders, catalog, shipping);
    }

    @Test
    @DisplayName("it builds a correct page, which is why nobody notices")
    void itBuildsTheRightPage() {
        OrderDetailsPage page = composer.pageFor(ORDER_ID);

        assertEquals(2, page.lines().size());
        assertEquals("Blue Stoneware Mug", page.lines().get(1).productName());
        assertEquals(Money.pence(3499 + 4 * 899), page.total());
        assertTrue(page.isComplete());
    }

    @Test
    @DisplayName("the shopper pays the sum of all three latencies")
    void itCostsTheSumOfTheLatencies() {
        composer.pageFor(ORDER_ID);

        assertEquals(OrderService.LATENCY_MILLIS + CatalogService.LATENCY_MILLIS
                + ShippingService.LATENCY_MILLIS, log.elapsedMillis());
        assertEquals(210, log.elapsedMillis());
    }

    @Test
    @DisplayName("no call starts before the one in front of it has finished")
    void nothingOverlaps() {
        composer.pageFor(ORDER_ID);

        var entries = log.entries();
        for (int i = 1; i < entries.size(); i++) {
            assertTrue(entries.get(i).startedAt() >= entries.get(i - 1).finishedAt(),
                    "call " + i + " overlapped the one before it");
        }
    }

    @Test
    @DisplayName("the last service failing throws away the answers already in hand")
    void itLosesWorkAlreadyDone() {
        shipping.goDown(1);

        assertThrows(ServiceUnavailableException.class, () -> composer.pageFor(ORDER_ID));

        // Both of these succeeded. Their answers went in the bin with the exception.
        assertEquals(1, orders.callsReceived());
        assertEquals(1, catalog.callsReceived());
        assertTrue(log.timeline().contains("Orders           OK"), log.timeline());
        assertTrue(log.timeline().contains("Catalog          OK"), log.timeline());
    }

    @Test
    @DisplayName("any one of the three failing takes the whole page with it")
    void allThreeAreEffectivelyRequired() {
        catalog.goDown(1);

        assertThrows(ServiceUnavailableException.class, () -> composer.pageFor(ORDER_ID));
        assertEquals(0, shipping.callsReceived());
    }
}
