package com.jk.explore.unitofwork.naive;

import com.jk.explore.unitofwork.domain.Order;
import com.jk.explore.unitofwork.domain.Product;
import com.jk.explore.unitofwork.toydb.Database;

import java.util.List;

/**
 * <strong>The version experienced readers reach for: wrap it in a
 * transaction.</strong> It mostly works, and it is shown working. Its cost
 * is that the transaction, and the locks it holds, stay open for the whole
 * computation, including the slow check made for each line.
 */
public class TransactionalPlacement extends SelfSavingPlacement {

    public TransactionalPlacement(Database db) {
        super(db);
    }

    @Override
    public void place(Order order, List<Product> products) {
        db.begin();
        try {
            super.place(order, products);
            db.commit();
        } catch (RuntimeException e) {
            db.rollback();
            throw e;
        }
    }

    /** Ticks the transaction is open: every slow check, plus every write. */
    @Override
    public int lockTicks(Order order) {
        return order.lines().size() * SLOW_CHECK_TICKS + super.lockTicks(order);
    }
}
