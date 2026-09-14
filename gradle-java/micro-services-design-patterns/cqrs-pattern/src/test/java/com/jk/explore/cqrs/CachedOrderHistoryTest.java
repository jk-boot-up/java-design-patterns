package com.jk.explore.cqrs;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The cache bolted on top of the composition, and every test in here passes.
 *
 * It is fast, it is fifteen lines, and it is the right answer surprisingly often. These
 * tests exist to write down the two things it cannot do, both of which are invisible to
 * "did it throw": it serves a page it has been told nothing about, and the only lever
 * anybody has over that is a timer.
 */
class CachedOrderHistoryTest {

    private static final String CUSTOMER = "cust-7";

    private SimulatedClock clock;
    private CallLog log;
    private EventBus events;
    private StockLedger stock;
    private CatalogService catalog;
    private OrderWriteService writeSide;
    private OrdersQueryApi orders;
    private CachedOrderHistory cached;

    @BeforeEach
    void setUp() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
        events = new EventBus(log);
        stock = new StockLedger(events);
        catalog = new CatalogService(events, clock, log);
        writeSide = new OrderWriteService(stock, events, clock, log);
        orders = new OrdersQueryApi(writeSide, clock, log);
        cached = new CachedOrderHistory(new ComposingOrderHistory(orders, catalog),
                clock, log);

        catalog.add("SKU-KETTLE", "Stainless Steel Kettle");
        stock.stock("SKU-KETTLE", 20);
        writeSide.place(CUSTOMER, List.of(new Order.Line("SKU-KETTLE", 1, Money.pence(3499))));
    }

    @Test
    @DisplayName("the first view composes and the rest are free")
    void itCachesThePage() {
        cached.historyFor(CUSTOMER);
        log.clear();

        cached.historyFor(CUSTOMER);
        cached.historyFor(CUSTOMER);

        assertEquals(2, cached.hits());
        assertEquals(1, cached.misses());
        assertEquals(0, log.elapsedMillis());
    }

    @Test
    @DisplayName("a new order is invisible for the whole expiry, not for a delivery lag")
    void itServesAPageItKnowsNothingAbout() {
        assertEquals(1, cached.historyFor(CUSTOMER).size());

        writeSide.place(CUSTOMER, List.of(new Order.Line("SKU-KETTLE", 2, Money.pence(3499))));

        // The order is placed and paid for. The cache was not told, and cannot be.
        assertEquals(1, cached.historyFor(CUSTOMER).size());
        clock.advance(CachedOrderHistory.EXPIRY_MILLIS / 2);
        assertEquals(1, cached.historyFor(CUSTOMER).size());
    }

    @Test
    @DisplayName("only the clock fixes it")
    void itIsCorrectedByATimerAndNothingElse() {
        cached.historyFor(CUSTOMER);
        writeSide.place(CUSTOMER, List.of(new Order.Line("SKU-KETTLE", 2, Money.pence(3499))));

        clock.advance(CachedOrderHistory.EXPIRY_MILLIS);

        assertEquals(2, cached.historyFor(CUSTOMER).size());
    }

    @Test
    @DisplayName("a rename does not reach the cache either")
    void aRenameCannotInvalidateIt() {
        cached.historyFor(CUSTOMER);

        catalog.rename("SKU-KETTLE", "Brushed Steel Kettle");

        assertEquals("Stainless Steel Kettle",
                cached.historyFor(CUSTOMER).get(0).productName());
    }

    @Test
    @DisplayName("a shorter expiry buys freshness by paying for the composition again")
    void thereIsNoFreeSetting() {
        log.clear();
        cached.historyFor(CUSTOMER);
        long firstViewCost = log.elapsedMillis();
        log.clear();

        clock.advance(CachedOrderHistory.EXPIRY_MILLIS);
        cached.historyFor(CUSTOMER);

        assertEquals(firstViewCost, log.elapsedMillis());
        assertTrue(firstViewCost >= OrdersQueryApi.LATENCY_MILLIS
                + CatalogService.LATENCY_MILLIS);
    }
}
