package com.jk.explore.databaseperservicecontainers;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.sql.SQLException;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

/**
 * What each engine really does, asked directly.
 *
 * <p>One Postgres and one MongoDB are started for the whole class, because starting them
 * is the slow part, and both are removed at the end. Each test builds its own fresh tables
 * and collection. There is no sleep anywhere in this file.
 */
class RealEnginesTest {

    private static final String CUSTOMER = DatabasePerServiceWithContainersDemo.CUSTOMER;
    private static Engines engines;

    @BeforeAll
    static void startBothEngines() {
        assumeTrue(Engines.containerRuntimeAvailable(), "needs a container runtime");
        engines = new Engines();
        engines.start();
    }

    @AfterAll
    static void stopBothEngines() {
        if (engines != null) {
            engines.close();
        }
    }

    private static SharedDatabase sharedShop() {
        SharedDatabase shop = new SharedDatabase(engines.postgres());
        shop.addProduct("SKU-KETTLE", "Stainless Steel Kettle");
        shop.addProduct("SKU-MUG", "Blue Stoneware Mug");
        shop.addOrder(new Order("ord-101", CUSTOMER, "SKU-KETTLE", 1));
        shop.addOrder(new Order("ord-102", CUSTOMER, "SKU-MUG", 4));
        return shop;
    }

    @Test
    void theSharedDatabaseAnswersThePageInOneJoin() throws SQLException {
        try (SharedDatabase shop = sharedShop()) {
            List<OrderHistoryRow> page = shop.orderHistory(CUSTOMER);
            assertEquals(2, page.size());
            assertEquals("Stainless Steel Kettle", page.get(0).productName());
            assertEquals(1, shop.roundTrips());
        }
    }

    @Test
    void theSharedDatabasesForeignKeyRefusesTheDelete() {
        try (SharedDatabase shop = sharedShop()) {
            SQLException refused = assertThrows(SQLException.class, () -> shop.deleteProduct("SKU-KETTLE"));
            assertEquals("23503", refused.getSQLState());
        }
    }

    @Test
    void aRenameInTheSharedDatabaseBreaksSomebodyElsesQuery() {
        try (SharedDatabase shop = sharedShop()) {
            shop.renameProductNameColumnTo("title");
            SQLException broken = assertThrows(SQLException.class, () -> shop.orderHistory(CUSTOMER));
            assertEquals("42703", broken.getSQLState());
            assertEquals("ERROR 42703: column p.product_name does not exist", SqlError.describe(broken));
        }
    }

    @Test
    void theSplitPageTakesTwoRoundTripsAndSurvivesTheRename() {
        try (DatabasePerServiceWithContainersDemo.Shop shop = new DatabasePerServiceWithContainersDemo.Shop(engines)) {
            List<OrderHistoryRow> before = shop.page.forCustomer(CUSTOMER);
            assertEquals(2, shop.roundTrips.count());
            assertEquals(2, shop.catalog.renameNameFieldTo("title"));
            assertEquals(before, shop.page.forCustomer(CUSTOMER));
        }
    }

    @Test
    void twoProductDocumentsCanHaveDifferentShapes() {
        try (DatabasePerServiceWithContainersDemo.Shop shop = new DatabasePerServiceWithContainersDemo.Shop(engines)) {
            assertEquals(List.of("_id", "name", "priceInPence", "stock", "wattage"), shop.catalog.fieldsOf("SKU-KETTLE"));
            assertEquals(List.of("_id", "name", "priceInPence", "stock", "capacityMl"), shop.catalog.fieldsOf("SKU-MUG"));
            assertEquals(1, shop.orders.tables());
        }
    }

    @Test
    void postgresRefusesTheJoinOutright() {
        try (SharedDatabase ignored = sharedShop();
             DatabasePerServiceWithContainersDemo.Shop shop = new DatabasePerServiceWithContainersDemo.Shop(engines)) {
            assertEquals("ERROR 42P01: relation \"products\" does not exist",
                    shop.orders.tryToRun("SELECT o.order_id, p.product_name FROM orders o JOIN products p ON p.sku = o.sku"));
            assertEquals("ERROR 0A000: cross-database references are not implemented: \"shop.public.products\"",
                    shop.orders.tryToRun("SELECT product_name FROM shop.public.products"));
        }
    }

    @Test
    void mongoDbsLookupIntoAMissingCollectionSaysNothingAndFindsNothing() {
        try (DatabasePerServiceWithContainersDemo.Shop shop = new DatabasePerServiceWithContainersDemo.Shop(engines)) {
            assertEquals(Map.of("SKU-KETTLE", 0, "SKU-MUG", 0), shop.catalog.tryToJoinOrders());
        }
    }

    @Test
    void nothingStopsCatalogDeletingAProductAnOrderStillNames() {
        try (DatabasePerServiceWithContainersDemo.Shop shop = new DatabasePerServiceWithContainersDemo.Shop(engines)) {
            assertEquals(1, shop.catalog.delete("SKU-KETTLE"));
            assertEquals(1, shop.orders.ordersNaming("SKU-KETTLE"));
            assertEquals(OrderHistoryPage.DELETED, shop.page.forCustomer(CUSTOMER).get(0).productName());
        }
    }

    @Test
    void aPostgresRollbackDoesNotReachMongoDb() {
        try (DatabasePerServiceWithContainersDemo.Shop shop = new DatabasePerServiceWithContainersDemo.Shop(engines)) {
            shop.orders.begin();
            shop.orders.insert(new Order("ord-103", CUSTOMER, "SKU-MUG", 2));
            shop.catalog.takeFromStock("SKU-MUG", 2);
            shop.orders.rollback();
            assertEquals(2, shop.orders.ordersFor(CUSTOMER).size());
            assertEquals(38, shop.catalog.stockOf("SKU-MUG"));
        }
    }
}
