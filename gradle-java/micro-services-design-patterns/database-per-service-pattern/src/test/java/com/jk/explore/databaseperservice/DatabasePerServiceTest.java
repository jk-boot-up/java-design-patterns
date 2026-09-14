package com.jk.explore.databaseperservice;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** Two databases: what it buys, and what it charges for it. */
class DatabasePerServiceTest {

    private static final String CUSTOMER = "cust-7";

    private SimulatedClock clock;
    private CallLog log;
    private OrderDatabase orderDatabase;
    private CatalogDatabase catalogDatabase;
    private OrderService orders;
    private CatalogService catalog;
    private OrderHistoryPage page;

    @BeforeEach
    void setUp() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
        orderDatabase = new OrderDatabase(log);
        catalogDatabase = new CatalogDatabase(log);
        orderDatabase.insert(new Order("ord-101", CUSTOMER, "SKU-KETTLE", 1));
        orderDatabase.insert(new Order("ord-102", CUSTOMER, "SKU-MUG", 4));
        catalogDatabase.insert("SKU-KETTLE", "Stainless Steel Kettle");
        catalogDatabase.insert("SKU-MUG", "Blue Stoneware Mug");
        orders = new OrderService(orderDatabase, clock, log);
        catalog = new CatalogService(catalogDatabase, clock, log);
        page = new OrderHistoryPage(orders, catalog, log);
    }

    @Test
    @DisplayName("the assembled page says the same thing the join said")
    void itProducesTheSamePage() {
        List<OrderHistoryRow> rows = page.forCustomer(CUSTOMER);

        assertEquals(2, rows.size());
        assertEquals("Stainless Steel Kettle", rows.get(0).productName());
        assertEquals("Blue Stoneware Mug", rows.get(1).productName());
    }

    @Test
    @DisplayName("nobody may read a database that is not theirs")
    void itRefusesCrossServiceReads() {
        assertThrows(NotYourDataException.class,
                () -> catalogDatabase.nameOf("Orders", "SKU-KETTLE"));
        assertThrows(NotYourDataException.class,
                () -> orderDatabase.ordersFor("Catalog", CUSTOMER));
    }

    @Test
    @DisplayName("the refusal is what makes the rename safe")
    void aRenameIsNowANonEvent() {
        catalogDatabase.renameProductNameColumnTo("title");

        List<OrderHistoryRow> rows = page.forCustomer(CUSTOMER);

        assertEquals(2, rows.size());
        assertEquals("Stainless Steel Kettle", rows.get(0).productName());
    }

    @Test
    @DisplayName("one page now costs two service calls instead of one query")
    void itCostsTwoCalls() {
        page.forCustomer(CUSTOMER);

        assertEquals(1, orders.callsReceived());
        assertEquals(1, catalog.callsReceived());
        assertEquals(OrderService.LATENCY_MILLIS + CatalogService.LATENCY_MILLIS,
                log.elapsedMillis());
    }

    @Test
    @DisplayName("catalog is asked once for many skus, not once per sku")
    void itAsksCatalogOnce() {
        orderDatabase.insert(new Order("ord-103", CUSTOMER, "SKU-KETTLE", 2));
        orderDatabase.insert(new Order("ord-104", CUSTOMER, "SKU-TOASTER", 1));
        catalogDatabase.insert("SKU-TOASTER", "Two Slice Toaster");

        assertEquals(4, page.forCustomer(CUSTOMER).size());
        assertEquals(1, catalog.callsReceived());
    }

    @Test
    @DisplayName("a page for a customer with no orders never troubles catalog")
    void itSkipsCatalogWhenThereIsNothingToName() {
        assertEquals(List.of(), page.forCustomer("cust-nobody"));
        assertEquals(0, catalog.callsReceived());
    }

    @Test
    @DisplayName("there is no foreign key any more, so an order can outlive its product")
    void anOrderCanReferToAProductThatIsGone() {
        catalogDatabase.delete("SKU-KETTLE");

        List<OrderHistoryRow> rows = page.forCustomer(CUSTOMER);

        // The page still renders. That is the good news and the bad news at once: the
        // rule that used to be impossible to break is now merely impolite to break.
        assertEquals(2, rows.size());
        assertEquals(CatalogService.UNKNOWN_PRODUCT, rows.get(0).productName());
    }

    @Test
    @DisplayName("each service's own database still counts its own queries")
    void eachDatabaseIsQueriedByItsOwnerOnly() {
        page.forCustomer(CUSTOMER);

        assertEquals(1, orderDatabase.queries());
        assertEquals(2, catalogDatabase.queries());
    }

    @Test
    @DisplayName("the timeline shows both services and the assembly between them")
    void theTimelineIsHonest() {
        page.forCustomer(CUSTOMER);

        // Orders is first because its call began before the query it contains. The
        // database line sits inside it, at the moment the query actually ran.
        assertEquals(List.of("Orders", "OrderDb", "Catalog", "HistoryPage"),
                log.services());
        assertTrue(log.timeline().contains("ASSEMBLED"));
    }

    @Test
    @DisplayName("a refused read is written into the timeline, not swallowed")
    void aRefusalIsLogged() {
        assertThrows(NotYourDataException.class,
                () -> orderDatabase.ordersFor("Catalog", CUSTOMER));

        assertTrue(log.timeline().contains("REFUSED"));
        assertEquals(0, orderDatabase.queries());
    }
}
