package com.jk.explore.unitofwork.naive;

import com.jk.explore.unitofwork.domain.Order;
import com.jk.explore.unitofwork.domain.OrderLine;
import com.jk.explore.unitofwork.domain.Product;
import com.jk.explore.unitofwork.domain.Shop;
import com.jk.explore.unitofwork.toydb.Database;

import java.util.List;

/**
 * <strong>Each object saves itself as it changes.</strong> Nothing groups
 * the writes, so a failure part-way through leaves whatever had already
 * been written.
 */
public class SelfSavingPlacement {

    /** The lock time, in ticks, of the slow check made for each line. */
    public static final int SLOW_CHECK_TICKS = 5;

    protected final Database db;

    public SelfSavingPlacement(Database db) {
        this.db = db;
    }

    public void place(Order order, List<Product> products) {
        db.table(Shop.ORDERS).insert(order.id(), Shop.orderRow(order));
        for (OrderLine line : order.lines()) {
            Product product = products.get(line.productId() - 1);
            product.take(line.quantity());
            db.table(Shop.PRODUCTS).update(product.id(), Shop.productRow(product));
            db.table(Shop.LINES).insert(line.id(), Shop.lineRow(line));
        }
    }

    /** Ticks the database spends locked: only the writes. */
    public int lockTicks(Order order) {
        return 1 + order.lines().size() * 2;
    }
}
