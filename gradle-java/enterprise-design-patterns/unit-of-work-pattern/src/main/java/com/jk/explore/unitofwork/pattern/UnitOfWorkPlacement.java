package com.jk.explore.unitofwork.pattern;

import com.jk.explore.unitofwork.domain.Order;
import com.jk.explore.unitofwork.domain.OrderLine;
import com.jk.explore.unitofwork.domain.Product;
import com.jk.explore.unitofwork.domain.Shop;
import com.jk.explore.unitofwork.toydb.Database;

import java.util.List;

/** Placing an order through a unit of work: change the objects, register them, commit once. */
public class UnitOfWorkPlacement {

    public static final List<String> INSERT_ORDER = List.of(Shop.ORDERS, Shop.LINES);

    private final Database db;

    public UnitOfWorkPlacement(Database db) {
        this.db = db;
    }

    /** Builds the change set. Nothing is written. */
    public UnitOfWork prepare(Order order, List<Product> products) {
        UnitOfWork work = new UnitOfWork(db, INSERT_ORDER);
        for (OrderLine line : order.lines()) {
            Product product = products.get(line.productId() - 1);
            product.take(line.quantity());
            work.registerDirty(Shop.PRODUCTS, product.id(), Shop.productRow(product));
            work.registerNew(Shop.LINES, line.id(), Shop.lineRow(line));
        }
        work.registerNew(Shop.ORDERS, order.id(), Shop.orderRow(order));
        return work;
    }

    /** Ticks the database is locked: the commit only. */
    public int lockTicks(Order order) {
        return 1 + order.lines().size() * 2;
    }
}
