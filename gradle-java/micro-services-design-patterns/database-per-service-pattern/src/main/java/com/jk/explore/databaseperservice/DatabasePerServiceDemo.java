package com.jk.explore.databaseperservice;

import java.util.List;

/**
 * Five acts. The shared database working, the shared database breaking, the split
 * databases doing the same job for more money, the same break turning into a
 * non-event, and the bill.
 */
public final class DatabasePerServiceDemo {

    private static final String CUSTOMER = "cust-7";

    private DatabasePerServiceDemo() {
    }

    public static void main(String[] args) {
        oneDatabaseWorkingWell();
        oneDatabaseBreaking();
        twoDatabasesDoingTheSameJob();
        theSameRenameNowHarmless();
        theBillForSplittingUp();
    }

    /** Act 1: one query, one join, a complete page. Nothing to complain about. */
    private static void oneDatabaseWorkingWell() {
        System.out.println("Act 1 - one database, one query");

        SharedSchema schema = sharedSchemaWithData();
        List<OrderHistoryRow> page = schema.orderHistory(CUSTOMER);

        print(page);
        System.out.println("  database round trips: " + schema.queriesForOnePage());
        System.out.println("  every row has a product name, because a join cannot"
                + " forget one");
        System.out.println();
    }

    /** Act 2: the catalog team renames a column they own. Somebody else's page dies. */
    private static void oneDatabaseBreaking() {
        System.out.println("Act 2 - the catalog team renames product_name to title");

        SharedSchema schema = sharedSchemaWithData();
        schema.renameProductNameColumnTo("title");
        System.out.println("  catalog team: migration ran, catalog tests green, done");

        try {
            schema.orderHistory(CUSTOMER);
            System.out.println("  order history page: fine");
        } catch (ColumnNotFoundException broken) {
            System.out.println("  order history page: " + broken.getMessage());
        }
        System.out.println("  nobody did anything wrong. The column was theirs.");
        System.out.println();
    }

    /** Act 3: two databases, two services, and the assembly step in the middle. */
    private static void twoDatabasesDoingTheSameJob() {
        System.out.println("Act 3 - two databases, two calls, one assembly");

        Shop shop = new Shop();
        List<OrderHistoryRow> page = shop.historyPage.forCustomer(CUSTOMER);

        print(page);
        System.out.print(shop.log.timeline());
        System.out.println("  the same page took " + shop.log.elapsedMillis()
                + "ms and 2 service calls instead of 1 query");
        System.out.println();
    }

    /** Act 4: the rename that broke act 2, run again where it cannot reach anybody. */
    private static void theSameRenameNowHarmless() {
        System.out.println("Act 4 - the same rename, against a database Catalog owns");

        Shop shop = new Shop();
        shop.catalogDatabase.renameProductNameColumnTo("title");
        List<OrderHistoryRow> page = shop.historyPage.forCustomer(CUSTOMER);

        print(page);
        System.out.println("  the page is unchanged. Nothing outside Catalog ever"
                + " named that column.");
        System.out.println();
    }

    /** Act 5: the two things the shop gave up to get act 4. */
    private static void theBillForSplittingUp() {
        System.out.println("Act 5 - what it cost");

        Shop shop = new Shop();

        System.out.println("  a) no more joining across the two sets of tables:");
        try {
            shop.catalogDatabase.nameOf("Orders", "SKU-KETTLE");
            System.out.println("     Orders read the product name directly");
        } catch (NotYourDataException refused) {
            System.out.println("     " + refused.getMessage());
        }

        System.out.println("  b) no more foreign key. Catalog deletes a product that"
                + " an order refers to:");
        shop.catalogDatabase.delete("SKU-KETTLE");
        List<OrderHistoryRow> page = shop.historyPage.forCustomer(CUSTOMER);
        print(page);
        System.out.println("     the row survives with no name. A foreign key would"
                + " have refused the delete.");
        System.out.println("     that rule now lives in code and in agreements"
                + " between teams, not in the database.");
        System.out.println();
    }

    private static void print(List<OrderHistoryRow> page) {
        for (OrderHistoryRow row : page) {
            System.out.printf("  %-9s %-12s %-28s x%d%n", row.orderId(), row.sku(),
                    row.productName(), row.quantity());
        }
    }

    private static SharedSchema sharedSchemaWithData() {
        SharedSchema schema = new SharedSchema();
        schema.addProduct("SKU-KETTLE", "Stainless Steel Kettle");
        schema.addProduct("SKU-MUG", "Blue Stoneware Mug");
        schema.addOrder(new Order("ord-101", CUSTOMER, "SKU-KETTLE", 1));
        schema.addOrder(new Order("ord-102", CUSTOMER, "SKU-MUG", 4));
        return schema;
    }

    /** The split-up shop, wired up once so each act can start from a clean one. */
    private static final class Shop {

        private final SimulatedClock clock = new SimulatedClock();
        private final CallLog log = new CallLog(clock);
        private final OrderDatabase orderDatabase = new OrderDatabase(log);
        private final CatalogDatabase catalogDatabase = new CatalogDatabase(log);
        private final OrderHistoryPage historyPage;

        private Shop() {
            orderDatabase.insert(new Order("ord-101", CUSTOMER, "SKU-KETTLE", 1));
            orderDatabase.insert(new Order("ord-102", CUSTOMER, "SKU-MUG", 4));
            catalogDatabase.insert("SKU-KETTLE", "Stainless Steel Kettle");
            catalogDatabase.insert("SKU-MUG", "Blue Stoneware Mug");
            historyPage = new OrderHistoryPage(
                    new OrderService(orderDatabase, clock, log),
                    new CatalogService(catalogDatabase, clock, log), log);
        }
    }
}
