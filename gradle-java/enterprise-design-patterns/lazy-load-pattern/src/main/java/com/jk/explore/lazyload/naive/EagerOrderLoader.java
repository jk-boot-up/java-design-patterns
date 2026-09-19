package com.jk.explore.lazyload.naive;

import com.jk.explore.lazyload.domain.Shop;
import com.jk.explore.lazyload.toydb.Database;
import com.jk.explore.lazyload.toydb.Row;

import java.util.HashSet;
import java.util.Set;

/**
 * <strong>Eager loading: everything reachable, immediately.</strong> An
 * order refers to its customer, the customer to their other orders, those to
 * their lines, the lines to products, the products to categories. There is no
 * cycle in it and no obvious mistake, and it still loads a great deal. Objects
 * are counted by their kind and id, so nothing is counted twice.
 */
public class EagerOrderLoader {

    private final Database db;
    private final Set<String> loaded = new HashSet<>();

    public EagerOrderLoader(Database db) {
        this.db = db;
    }

    /** Loads the order and everything reachable from it. Returns how many objects that was. */
    public int load(int orderId) {
        loadOrder(orderId);
        return loaded.size();
    }

    private void loadOrder(int orderId) {
        if (!loaded.add("order " + orderId)) {
            return;
        }
        Row order = db.table(Shop.ORDERS).select(orderId);
        int customerId = order.number("customer_id");
        if (loaded.add("customer " + customerId)) {
            db.table(Shop.CUSTOMERS).select(customerId);
            for (Row other : db.table(Shop.ORDERS).selectWhere("customer_id", customerId)) {
                loadOrder(other.number("id"));
            }
        }
        for (Row line : db.table(Shop.LINES).selectWhere("order_id", orderId)) {
            loaded.add("line " + line.number("id"));
            int productId = line.number("product_id");
            if (loaded.add("product " + productId)) {
                Row product = db.table(Shop.PRODUCTS).select(productId);
                int categoryId = product.number("category_id");
                if (loaded.add("category " + categoryId)) {
                    db.table(Shop.CATEGORIES).select(categoryId);
                }
            }
        }
    }
}
