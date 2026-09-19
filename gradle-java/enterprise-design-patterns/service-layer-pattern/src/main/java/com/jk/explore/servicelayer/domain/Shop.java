package com.jk.explore.servicelayer.domain;

import com.jk.explore.servicelayer.toydb.Database;
import com.jk.explore.servicelayer.toydb.Row;

import java.util.ArrayList;
import java.util.List;

/** The seeded store: three products, and the way a product becomes a row. */
public final class Shop {

    public static final String PRODUCTS = "products";
    public static final String ORDERS = "orders";

    private Shop() {
    }

    public static List<Product> products() {
        return new ArrayList<>(List.of(
                new Product(1, "Keyboard", 2_500, 10),
                new Product(2, "Mouse", 1_200, 3),
                new Product(3, "Monitor", 15_000, 5)));
    }

    public static Database seeded() {
        Database db = new Database();
        db.requireParent("order_lines", "order_id", ORDERS);
        for (Product p : products()) {
            db.table(PRODUCTS).insert(p.id(), productRow(p));
        }
        db.clearLog();
        return db;
    }

    public static Row productRow(Product p) {
        return Row.of("name", p.name(), "price", p.pricePence(), "stock", p.stock());
    }

    public static int stockOf(Database db, int productId) {
        return db.table(PRODUCTS).peek(productId).number("stock");
    }
}
