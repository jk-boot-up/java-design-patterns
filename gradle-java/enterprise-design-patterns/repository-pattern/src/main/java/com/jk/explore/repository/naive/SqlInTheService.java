package com.jk.explore.repository.naive;

import com.jk.explore.repository.domain.Shop;
import com.jk.explore.repository.toydb.Database;
import com.jk.explore.repository.toydb.Row;

import java.util.ArrayList;
import java.util.List;

/**
 * <strong>The query lives in the service, and is written where it is needed.</strong>
 * This is how most code starts, and for one query in one place it is fine.
 * Here the same question, London customers who ordered in the last month, is
 * asked from three different services, each written slightly differently, and
 * one of them is subtly wrong. The column name {@code city} is a string in all
 * three.
 */
public class SqlInTheService {

    private final Database db;

    public SqlInTheService(Database db) {
        this.db = db;
    }

    /** The marketing team's version: correct. */
    public List<String> marketingList() {
        List<String> names = new ArrayList<>();
        for (Row customer : db.table("customers").selectWhere("city", "London")) {
            for (Row order : db.table("orders").selectWhere("customer_id", customer.number("id"))) {
                if (order.number("day") > Shop.LAST_MONTH_STARTS) {
                    names.add(customer.text("name"));
                    break;
                }
            }
        }
        return names;
    }

    /** The support team's version: written a little differently, and off by one day. */
    public List<String> supportList() {
        List<String> names = new ArrayList<>();
        for (Row customer : db.table("customers").selectWhere("city", "London")) {
            for (Row order : db.table("orders").selectWhere("customer_id", customer.number("id"))) {
                if (order.number("day") >= Shop.LAST_MONTH_STARTS) {
                    names.add(customer.text("name"));
                    break;
                }
            }
        }
        return names;
    }

    /** The reporting version: starts from the orders instead. Correct, but a third way of asking. */
    public List<String> reportList() {
        List<String> names = new ArrayList<>();
        for (Row order : db.table("orders").selectAll()) {
            if (order.number("day") > Shop.LAST_MONTH_STARTS) {
                Row customer = db.table("customers").select(order.number("customer_id"));
                if ("London".equals(customer.text("city")) && !names.contains(customer.text("name"))) {
                    names.add(customer.text("name"));
                }
            }
        }
        return names;
    }
}
