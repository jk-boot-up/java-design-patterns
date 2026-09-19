package com.jk.explore.lazyload.domain;

import com.jk.explore.lazyload.toydb.Database;
import com.jk.explore.lazyload.toydb.Row;

/**
 * The seeded store: 5 customers with 4 orders each, 4 lines per order, 12
 * products in 4 categories. Order ids run 1 to 20; order {@code n} belongs to
 * customer {@code (n-1)/4 + 1}.
 */
public final class Shop {

    public static final String CUSTOMERS = "customers";
    public static final String ORDERS = "orders";
    public static final String LINES = "order_lines";
    public static final String PRODUCTS = "products";
    public static final String CATEGORIES = "categories";

    private Shop() {
    }

    public static Database seeded() {
        Database db = new Database();
        for (int c = 1; c <= 4; c++) {
            db.table(CATEGORIES).insert(c, Row.of("id", c, "name", "Category " + c));
        }
        for (int p = 1; p <= 12; p++) {
            db.table(PRODUCTS).insert(p, Row.of("id", p, "name", "Product " + p, "category_id", (p - 1) % 4 + 1));
        }
        for (int c = 1; c <= 5; c++) {
            db.table(CUSTOMERS).insert(c, Row.of("id", c, "name", "Customer " + c));
        }
        int line = 1;
        for (int o = 1; o <= 20; o++) {
            db.table(ORDERS).insert(o, Row.of("id", o, "customer_id", (o - 1) / 4 + 1));
            for (int l = 0; l < 4; l++) {
                db.table(LINES).insert(line, Row.of("id", line, "order_id", o, "product_id", (line - 1) % 12 + 1, "quantity", 1));
                line++;
            }
        }
        db.clearLog();
        return db;
    }
}
