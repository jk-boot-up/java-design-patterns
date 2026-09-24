package com.jk.explore.databaseperservicecontainers;

import java.sql.SQLException;
import java.util.List;
import java.util.Map;
import org.bson.Document;

/**
 * Six acts against a real PostgreSQL and a real MongoDB, both started and stopped by this
 * program.
 *
 * <p>The shop's Orders and Catalog teams first share one Postgres database, and it works
 * and then breaks. Then each service gets a database of its own on a different engine:
 * Orders keeps Postgres, Catalog moves to MongoDB. The rest shows what that buys, what the
 * old join turns into, and what it costs.
 */
public class DatabasePerServiceWithContainersDemo {

    static final String CUSTOMER = "cust-7";

    public static void main(String[] args) {
        if (!Engines.containerRuntimeAvailable()) {
            System.out.println(Engines.NO_RUNTIME_ADVICE);
            return;
        }
        try (Engines engines = new Engines()) {
            try {
                engines.start();
            } catch (RuntimeException e) {
                System.out.println(Engines.WOULD_NOT_START_ADVICE);
                return;
            }
            one(engines.postgres());
            two(engines.postgres());
            three(engines);
            four(engines);
            five(engines);
            six(engines);
        }
    }

    /** One Postgres database holding both teams' tables. One join, and a foreign key that holds. */
    private static void one(Postgres postgres) {
        System.out.println("ONE. One shared database: Postgres, holding both teams' tables.");
        try (SharedDatabase shop = sharedShop(postgres)) {
            System.out.println("  database shop: products belongs to Catalog, orders belongs to Orders, and a foreign key ties them together.");
            System.out.println("  the order history page for " + CUSTOMER + " is one SQL join:");
            print(shop.orderHistory(CUSTOMER));
            System.out.println("  round trips to a database: " + shop.roundTrips());
            System.out.println("  Catalog tries to delete SKU-KETTLE, which ord-101 still names. Postgres refuses:");
            try {
                shop.deleteProduct("SKU-KETTLE");
                System.out.println("    deleted");
            } catch (SQLException refused) {
                System.out.println("    " + SqlError.describe(refused));
            }
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    /** The Catalog team renames a column it owns. The Orders team's page dies. */
    private static void two(Postgres postgres) {
        System.out.println("TWO. The Catalog team renames product_name to title.");
        try (SharedDatabase shop = sharedShop(postgres)) {
            shop.renameProductNameColumnTo("title");
            System.out.println("  ALTER TABLE products RENAME COLUMN product_name TO title: done. Catalog's own queries updated, its tests green.");
            System.out.println("  the order history page, which belongs to Orders:");
            try {
                shop.orderHistory(CUSTOMER);
                System.out.println("    fine");
            } catch (SQLException broken) {
                System.out.println("    " + SqlError.describe(broken));
            }
            System.out.println("  nobody did anything wrong. the column was Catalog's; the query naming it was Orders'.");
        }
    }

    /** Each service on its own engine. The page takes two questions, and the rename is harmless. */
    private static void three(Engines engines) {
        System.out.println("THREE. Two services, two engines.");
        try (Shop shop = new Shop(engines)) {
            System.out.println("  Orders owns the orders database on Postgres 18.6: " + shop.orders.tables() + " table.");
            System.out.println("  Catalog owns the catalog database on MongoDB 8.3.11: 1 collection of documents.");
            System.out.println("  two products, two shapes, and no table to change first:");
            System.out.println("    SKU-KETTLE: " + String.join(", ", shop.catalog.fieldsOf("SKU-KETTLE")));
            System.out.println("    SKU-MUG: " + String.join(", ", shop.catalog.fieldsOf("SKU-MUG")));
            System.out.println("  the order history page: one SQL query to Orders, one find to Catalog for both skus, put together in Java:");
            print(shop.page.forCustomer(CUSTOMER));
            System.out.println("  round trips to a database: " + shop.roundTrips.count());
            long changed = shop.catalog.renameNameFieldTo("title");
            System.out.println("  Catalog renames name to title in every document: MongoDB changed " + changed
                    + " documents. Catalog's own code reads title from now on.");
            print(shop.page.forCustomer(CUSTOMER));
            System.out.println("  the page is unchanged. nothing outside Catalog ever named that field.");
        }
    }

    /** The old join, tried from both sides. One engine refuses loudly; the other says nothing. */
    private static void four(Engines engines) {
        System.out.println("FOUR. The join, tried anyway.");
        try (SharedDatabase ignored = sharedShop(engines.postgres()); Shop shop = new Shop(engines)) {
            System.out.println("  from Orders, the old SQL join:");
            System.out.println("    " + shop.orders.tryToRun(
                    "SELECT o.order_id, p.product_name FROM orders o JOIN products p ON p.sku = o.sku"));
            System.out.println("  from Orders, reaching across to the shop database on the same Postgres server:");
            System.out.println("    " + shop.orders.tryToRun("SELECT product_name FROM shop.public.products"));
            System.out.println("  from Catalog, MongoDB's own join, $lookup, into a collection called orders:");
            Map<String, Integer> attached = shop.catalog.tryToJoinOrders();
            StringBuilder each = new StringBuilder();
            for (Map.Entry<String, Integer> e : attached.entrySet()) {
                each.append(each.isEmpty() ? "" : ", ").append(e.getKey()).append(" with ").append(e.getValue()).append(" orders");
            }
            System.out.println("    no error. " + attached.size() + " products came back: " + each + ".");
            System.out.println("    MongoDB has no collection called orders, so it treated it as empty and said nothing.");
            System.out.println("  no engine holds both halves. the join is not forbidden; it cannot be written.");
        }
    }

    /** No foreign key can reach from one engine into another. The delete goes through. */
    private static void five(Engines engines) {
        System.out.println("FIVE. No foreign key between two engines.");
        try (Shop shop = new Shop(engines)) {
            long deleted = shop.catalog.delete("SKU-KETTLE");
            System.out.println("  Catalog deletes SKU-KETTLE: MongoDB deleted " + deleted + " document. nothing refused.");
            System.out.println("  Postgres still holds " + shop.orders.ordersNaming("SKU-KETTLE") + " order naming SKU-KETTLE.");
            print(shop.page.forCustomer(CUSTOMER));
            System.out.println("  in act ONE Postgres refused this delete. across two engines nothing can.");
        }
    }

    /** No transaction spans two engines, and either engine can be down while the other is up. */
    private static void six(Engines engines) {
        System.out.println("SIX. The bill.");
        try (Shop shop = new Shop(engines)) {
            int stockBefore = shop.catalog.stockOf("SKU-MUG");
            System.out.println("  " + CUSTOMER + " checks out 2 more mugs. Orders writes ord-103 inside a Postgres transaction;"
                    + " Catalog takes 2 mugs from stock in MongoDB.");
            shop.orders.begin();
            shop.orders.insert(new Order("ord-103", CUSTOMER, "SKU-MUG", 2));
            shop.catalog.takeFromStock("SKU-MUG", 2);
            System.out.println("  the payment is declined, so Orders rolls back.");
            shop.orders.rollback();
            System.out.println("  Postgres: ord-103 is gone. orders for " + CUSTOMER + ": "
                    + shop.orders.ordersFor(CUSTOMER).size() + ".");
            System.out.println("  MongoDB: SKU-MUG stock " + shop.catalog.stockOf("SKU-MUG") + ", was " + stockBefore
                    + ". the rollback reached one engine, not both.");

            engines.mongo().stop();
            System.out.println("  MongoDB is stopped. the order history page for " + CUSTOMER + ":");
            print(shop.page.forCustomer(CUSTOMER));
            System.out.println("  Orders still answered; Catalog did not. the page is half there.");
            System.out.println("  this demo runs 2 containers, 2 drivers and 2 query languages, where the shared database had 1 of each.");
        }
    }

    private static void print(List<OrderHistoryRow> page) {
        for (OrderHistoryRow row : page) {
            System.out.println("    " + row.printed());
        }
    }

    private static SharedDatabase sharedShop(Postgres postgres) {
        SharedDatabase shop = new SharedDatabase(postgres);
        shop.addProduct("SKU-KETTLE", "Stainless Steel Kettle");
        shop.addProduct("SKU-MUG", "Blue Stoneware Mug");
        shop.addOrder(new Order("ord-101", CUSTOMER, "SKU-KETTLE", 1));
        shop.addOrder(new Order("ord-102", CUSTOMER, "SKU-MUG", 4));
        return shop;
    }

    /** The split-up shop: two services, each with a connection to its own engine and no other. */
    static final class Shop implements AutoCloseable {

        final RoundTrips roundTrips = new RoundTrips();
        final OrderService orders;
        final CatalogService catalog;
        final OrderHistoryPage page;

        Shop(Engines engines) {
            orders = new OrderService(engines.postgres(), roundTrips);
            catalog = new CatalogService(engines.mongo(), roundTrips);
            orders.insert(new Order("ord-101", CUSTOMER, "SKU-KETTLE", 1));
            orders.insert(new Order("ord-102", CUSTOMER, "SKU-MUG", 4));
            catalog.add("SKU-KETTLE", "Stainless Steel Kettle", 3499, 12, new Document("wattage", 3000));
            catalog.add("SKU-MUG", "Blue Stoneware Mug", 899, 40, new Document("capacityMl", 350));
            page = new OrderHistoryPage(orders, catalog);
        }

        @Override
        public void close() {
            catalog.close();
            orders.close();
        }
    }
}
