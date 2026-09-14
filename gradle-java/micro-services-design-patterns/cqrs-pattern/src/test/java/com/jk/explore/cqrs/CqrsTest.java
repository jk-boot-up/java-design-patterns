package com.jk.explore.cqrs;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** The read model: what it costs, when it is wrong, and what it must not be used for. */
class CqrsTest {

    private static final String CUSTOMER = "cust-7";

    private SimulatedClock clock;
    private CallLog log;
    private EventBus events;
    private List<ShopEvent> recorded;
    private StockLedger stock;
    private CatalogService catalog;
    private OrderWriteService writeSide;
    private OrdersQueryApi orders;
    private OrderHistoryReadModel readModel;
    private ComposingOrderHistory composing;

    @BeforeEach
    void setUp() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
        events = new EventBus(log);
        recorded = new ArrayList<>();
        stock = new StockLedger(events);
        catalog = new CatalogService(events, clock, log);
        writeSide = new OrderWriteService(stock, events, clock, log);
        orders = new OrdersQueryApi(writeSide, clock, log);
        readModel = new OrderHistoryReadModel(catalog, clock, log);
        events.subscribe(recorded::add);
        readModel.listenTo(events);
        composing = new ComposingOrderHistory(orders, catalog);

        catalog.add("SKU-KETTLE", "Stainless Steel Kettle");
        catalog.add("SKU-MUG", "Blue Stoneware Mug");
        stock.stock("SKU-KETTLE", 20);
        stock.stock("SKU-MUG", 50);
    }

    private Order placeAnOrder() {
        return writeSide.place(CUSTOMER, List.of(
                new Order.Line("SKU-KETTLE", 1, Money.pence(3499)),
                new Order.Line("SKU-MUG", 4, Money.pence(899))));
    }

    @Test
    @DisplayName("the read model and the composed page say the same thing")
    void bothSidesAgreeWhenEverythingHasBeenDelivered() {
        placeAnOrder();

        List<OrderHistoryRow> ready = readModel.historyFor(CUSTOMER);
        List<OrderHistoryRow> composed = composing.historyFor(CUSTOMER);

        assertEquals(2, ready.size());
        assertEquals(composed.size(), ready.size());
        assertEquals(composed.get(0).productName(), ready.get(0).productName());
        assertEquals(composed.get(0).lineTotal(), ready.get(0).lineTotal());
    }

    @Test
    @DisplayName("a page view calls nobody and costs one lookup")
    void aReadCostsOneLookup() {
        placeAnOrder();
        int callsAfterTheWrite = catalog.callsReceived() + orders.callsReceived();
        log.clear();

        readModel.historyFor(CUSTOMER);
        readModel.historyFor(CUSTOMER);
        readModel.historyFor(CUSTOMER);

        assertEquals(3 * OrderHistoryReadModel.LOOKUP_MILLIS, log.elapsedMillis());
        assertEquals(callsAfterTheWrite, catalog.callsReceived() + orders.callsReceived());
    }

    @Test
    @DisplayName("composing the same three views costs both services three times over")
    void composingPaysEveryTime() {
        placeAnOrder();
        log.clear();

        composing.historyFor(CUSTOMER);
        composing.historyFor(CUSTOMER);
        composing.historyFor(CUSTOMER);

        assertEquals(3, orders.callsReceived());
        assertEquals(3 * (OrdersQueryApi.LATENCY_MILLIS + CatalogService.LATENCY_MILLIS),
                log.elapsedMillis());
        assertTrue(log.elapsedMillis() > 3 * OrderHistoryReadModel.LOOKUP_MILLIS * 10);
    }

    @Test
    @DisplayName("the work moved to the write, it did not disappear")
    void theCostMovesToTheWriteSide() {
        assertEquals(0, catalog.callsReceived());

        placeAnOrder();

        assertEquals(1, catalog.callsReceived());
    }

    @Test
    @DisplayName("a customer can place an order and not see it")
    void theStalenessWindowIsReal() {
        events.holdEvents();

        Order placed = placeAnOrder();

        assertEquals(CUSTOMER, placed.customerId());
        assertEquals(0, readModel.historyFor(CUSTOMER).size());
        assertTrue(events.undelivered() > 0);
    }

    @Test
    @DisplayName("the window closes when the events arrive, without anybody retrying")
    void theWindowClosesByItself() {
        events.holdEvents();
        placeAnOrder();

        events.deliverHeld();

        assertEquals(2, readModel.historyFor(CUSTOMER).size());
        assertEquals(0, events.undelivered());
    }

    @Test
    @DisplayName("a rename reaches the copies the read model is holding")
    void itAppliesRenames() {
        placeAnOrder();

        catalog.rename("SKU-KETTLE", "Brushed Steel Kettle");

        assertEquals("Brushed Steel Kettle",
                readModel.historyFor(CUSTOMER).get(0).productName());
    }

    @Test
    @DisplayName("the read model still answers when Catalog is down")
    void readsSurviveAnOutage() {
        placeAnOrder();
        catalog.goDown(5);

        assertEquals(2, readModel.historyFor(CUSTOMER).size());
        assertThrows(ServiceUnavailableException.class,
                () -> composing.historyFor(CUSTOMER));
    }

    @Test
    @DisplayName("the stock number on the read model goes stale")
    void displayStockGoesStale() {
        events.holdEvents();

        writeSide.place(CUSTOMER, List.of(new Order.Line("SKU-KETTLE", 5, Money.pence(3499))));

        assertEquals(15, stock.available("SKU-KETTLE"));
        assertEquals(20, readModel.stockOnDisplay("SKU-KETTLE"));
        assertNotEquals(stock.available("SKU-KETTLE"),
                readModel.stockOnDisplay("SKU-KETTLE"));
    }

    @Test
    @DisplayName("the ledger refuses the last kettle twice even when the display says yes")
    void theWriteSideIsWhereASaleIsDecided() {
        stock.stock("SKU-KETTLE", 1);
        events.holdEvents();
        writeSide.place(CUSTOMER, List.of(new Order.Line("SKU-KETTLE", 1, Money.pence(3499))));

        // The read model is still advertising one on the shelf. A checkout that trusted
        // it would sell the same kettle twice.
        assertEquals(1, readModel.stockOnDisplay("SKU-KETTLE"));
        assertThrows(OutOfStockException.class, () -> writeSide.place("cust-9",
                List.of(new Order.Line("SKU-KETTLE", 1, Money.pence(3499)))));
    }

    @Test
    @DisplayName("the read model can be thrown away and rebuilt from the events")
    void itRebuilds() {
        placeAnOrder();
        catalog.rename("SKU-KETTLE", "Brushed Steel Kettle");
        List<OrderHistoryRow> before = readModel.historyFor(CUSTOMER);

        readModel.rebuildFrom(List.copyOf(recorded));

        List<OrderHistoryRow> after = readModel.historyFor(CUSTOMER);
        assertEquals(before.size(), after.size());
        assertEquals("Brushed Steel Kettle", after.get(0).productName());
        // Fifty on the shelf, four sold, and the replay lands on the same number.
        assertEquals(46, readModel.stockOnDisplay("SKU-MUG"));
    }

    @Test
    @DisplayName("the write side does not know the read model exists")
    void theWriteSideIsIndependent() {
        EventBus lonelyBus = new EventBus(log);
        StockLedger lonelyStock = new StockLedger(lonelyBus);
        lonelyStock.stock("SKU-KETTLE", 3);
        OrderWriteService lonely =
                new OrderWriteService(lonelyStock, lonelyBus, clock, log);

        Order placed = lonely.place(CUSTOMER,
                List.of(new Order.Line("SKU-KETTLE", 1, Money.pence(3499))));

        assertEquals(1, lonely.allOrders().size());
        assertEquals(CUSTOMER, placed.customerId());
    }
}
