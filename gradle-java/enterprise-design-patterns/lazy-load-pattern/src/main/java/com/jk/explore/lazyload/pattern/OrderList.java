package com.jk.explore.lazyload.pattern;

import com.jk.explore.lazyload.domain.Shop;
import com.jk.explore.lazyload.toydb.Database;
import com.jk.explore.lazyload.toydb.Row;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** A page listing orders with each customer's name, loaded two ways. */
public class OrderList {

    private final Database db;

    public OrderList(Database db) {
        this.db = db;
    }

    /** Lazy: one query for the orders, then one query per order for its customer. This is N+1. */
    public List<String> lazy() {
        Session session = new Session(db);
        List<String> lines = new ArrayList<>();
        for (Row order : db.table(Shop.ORDERS).selectAll()) {
            lines.add("order " + order.number("id") + " for "
                    + new CustomerProxy(session, order.number("customer_id")).name());
        }
        return lines;
    }

    /** Batched: one query for the orders, one for all the customers. */
    public List<String> batched() {
        Map<Integer, String> names = new HashMap<>();
        List<Row> orders = db.table(Shop.ORDERS).selectAll();
        for (Row customer : db.table(Shop.CUSTOMERS).selectAll()) {
            names.put(customer.number("id"), customer.text("name"));
        }
        List<String> lines = new ArrayList<>();
        for (Row order : orders) {
            lines.add("order " + order.number("id") + " for " + names.get(order.number("customer_id")));
        }
        return lines;
    }
}
