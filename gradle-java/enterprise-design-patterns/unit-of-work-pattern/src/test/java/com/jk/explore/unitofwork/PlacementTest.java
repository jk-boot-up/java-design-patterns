package com.jk.explore.unitofwork;

import com.jk.explore.unitofwork.domain.Order;
import com.jk.explore.unitofwork.domain.Shop;
import com.jk.explore.unitofwork.naive.SelfSavingPlacement;
import com.jk.explore.unitofwork.naive.TransactionalPlacement;
import com.jk.explore.unitofwork.toydb.Database;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PlacementTest {

    @Test
    void selfSavingObjectsLeaveAnOrderWithTwoLinesAndWrongStock() {
        Database db = Shop.seeded();
        db.failWriteNumber(OrderDemo.THIRD_STOCK_UPDATE);
        assertThrows(IllegalStateException.class,
                () -> new SelfSavingPlacement(db).place(Shop.threeLineOrder(), Shop.products()));
        assertEquals(1, db.table(Shop.ORDERS).size());
        assertEquals(2, db.table(Shop.LINES).size());
        assertEquals(8, Shop.stockOf(db, 1));
        assertEquals(9, Shop.stockOf(db, 2));
        assertEquals(10, Shop.stockOf(db, 3));
    }

    @Test
    void aTransactionUndoesItButStaysOpenForTheWholeComputation() {
        Database db = Shop.seeded();
        db.failWriteNumber(OrderDemo.THIRD_STOCK_UPDATE);
        Order order = Shop.threeLineOrder();
        TransactionalPlacement placement = new TransactionalPlacement(db);
        assertThrows(IllegalStateException.class, () -> placement.place(order, Shop.products()));
        assertEquals(0, db.table(Shop.ORDERS).size());
        assertEquals(0, db.table(Shop.LINES).size());
        assertEquals(10, Shop.stockOf(db, 1));
        assertEquals(22, placement.lockTicks(order));
        assertTrue(placement.lockTicks(order) > new SelfSavingPlacement(db).lockTicks(order));
    }
}
