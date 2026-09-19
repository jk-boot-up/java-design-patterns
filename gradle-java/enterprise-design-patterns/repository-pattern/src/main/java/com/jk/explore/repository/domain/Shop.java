package com.jk.explore.repository.domain;

import com.jk.explore.repository.toydb.Database;
import com.jk.explore.repository.toydb.Row;

import java.util.List;

/**
 * The seeded store. Today is day 100, so "ordered in the last month" means
 * an order on a day after {@link #LAST_MONTH_STARTS}, that is, days 71 to 100.
 */
public final class Shop {

    public static final int TODAY = 100;
    public static final int LAST_MONTH_STARTS = 70;

    private Shop() {
    }

    public static List<Customer> customers() {
        Customer ada = new Customer(1, "Ada", "London");
        ada.orders().add(new Order(1, 95, "SHIPPED"));
        ada.orders().add(new Order(2, 40, "SHIPPED"));
        Customer grace = new Customer(2, "Grace", "London");
        grace.orders().add(new Order(3, 60, "PENDING"));
        grace.orders().add(new Order(4, 99, "PENDING"));
        Customer linus = new Customer(3, "Linus", "Leeds");
        linus.orders().add(new Order(5, 98, "SHIPPED"));
        Customer ken = new Customer(4, "Ken", "London");
        ken.orders().add(new Order(6, 70, "SHIPPED"));
        Customer dennis = new Customer(5, "Dennis", "Leeds");
        Customer barbara = new Customer(6, "Barbara", "London");
        barbara.orders().add(new Order(7, 10, "SHIPPED"));
        return List.of(ada, grace, linus, ken, dennis, barbara);
    }

    public static Database seeded() {
        Database db = new Database();
        for (Customer c : customers()) {
            db.table("customers").insert(c.id(), Row.of("id", c.id(), "name", c.name(), "city", c.city()));
            for (Order o : c.orders()) {
                db.table("orders").insert(o.id(), Row.of("id", o.id(), "customer_id", c.id(), "day", o.day(), "status", o.status()));
            }
        }
        db.clearLog();
        return db;
    }
}
