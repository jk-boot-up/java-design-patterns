package com.jk.explore.unitofwork.domain;

import com.jk.explore.unitofwork.toydb.Database;
import com.jk.explore.unitofwork.toydb.Row;

import java.util.List;

/** The seeded store, and how domain objects become rows. One place, so every demo tells the same story. */
public final class Shop {

    public static final String PRODUCTS = "products";
    public static final String ORDERS = "orders";
    public static final String LINES = "order_lines";

    private Shop() {
    }

    public static Database seeded() {
        Database db = new Database();
        db.requireParent(LINES, "order_id", ORDERS);
        db.table(PRODUCTS).insert(1, productRow(new Product(1, "Keyboard", 10)));
        db.table(PRODUCTS).insert(2, productRow(new Product(2, "Mouse", 10)));
        db.table(PRODUCTS).insert(3, productRow(new Product(3, "Monitor", 10)));
        db.clearLog();
        return db;
    }

    public static List<Product> products() {
        return List.of(new Product(1, "Keyboard", 10), new Product(2, "Mouse", 10), new Product(3, "Monitor", 10));
    }

    public static Order threeLineOrder() {
        Order order = new Order(100, 7);
        order.addLine(1, 2);
        order.addLine(2, 1);
        order.addLine(3, 1);
        return order;
    }

    public static Row productRow(Product p) {
        return Row.of("name", p.name(), "stock", p.stock());
    }

    public static Row orderRow(Order o) {
        return Row.of("customer_id", o.customerId());
    }

    public static Row lineRow(OrderLine l) {
        return Row.of("order_id", l.orderId(), "product_id", l.productId(), "quantity", l.quantity());
    }

    public static int stockOf(Database db, int productId) {
        return db.table(PRODUCTS).peek(productId).number("stock");
    }
}
