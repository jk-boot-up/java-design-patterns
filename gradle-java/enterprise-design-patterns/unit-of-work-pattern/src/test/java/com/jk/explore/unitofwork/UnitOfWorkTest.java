package com.jk.explore.unitofwork;

import com.jk.explore.unitofwork.domain.Order;
import com.jk.explore.unitofwork.domain.Product;
import com.jk.explore.unitofwork.domain.Shop;
import com.jk.explore.unitofwork.naive.TransactionalPlacement;
import com.jk.explore.unitofwork.pattern.UnitOfWork;
import com.jk.explore.unitofwork.pattern.UnitOfWorkPlacement;
import com.jk.explore.unitofwork.toydb.Database;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class UnitOfWorkTest {

    @Test
    void nothingTouchesTheDatabaseUntilCommit() {
        Database db = Shop.seeded();
        UnitOfWork work = new UnitOfWorkPlacement(db).prepare(Shop.threeLineOrder(), Shop.products());
        assertEquals(0, db.operationCount());
        assertEquals(7, work.pendingChanges());
        assertEquals(0, db.table(Shop.ORDERS).size());
        work.commit();
        assertEquals(1, db.table(Shop.ORDERS).size());
        assertEquals(3, db.table(Shop.LINES).size());
        assertEquals(8, Shop.stockOf(db, 1));
    }

    @Test
    void commitWritesTheOrderBeforeItsLinesWhateverTheRegistrationOrder() {
        Database db = Shop.seeded();
        new UnitOfWorkPlacement(db).prepare(Shop.threeLineOrder(), Shop.products()).commit();
        assertEquals("INSERT orders id=100", db.operations().get(0));
    }

    @Test
    void writingInRegistrationOrderBreaksTheForeignKey() {
        Database db = Shop.seeded();
        UnitOfWork work = new UnitOfWorkPlacement(db).prepare(Shop.threeLineOrder(), Shop.products());
        assertThrows(IllegalStateException.class, work::commitInRegistrationOrder);
        assertEquals(0, db.table(Shop.LINES).size(), "and the failed attempt was rolled back");
    }

    @Test
    void aFailureAtTheThirdStockUpdateRollsBackToExactlyWhatWasThere() {
        Database db = Shop.seeded();
        db.failWriteNumber(OrderDemo.THIRD_STOCK_UPDATE_AT_COMMIT);
        UnitOfWork work = new UnitOfWorkPlacement(db).prepare(Shop.threeLineOrder(), Shop.products());
        assertThrows(IllegalStateException.class, work::commit);
        assertEquals(0, db.table(Shop.ORDERS).size());
        assertEquals(0, db.table(Shop.LINES).size());
        assertEquals(10, Shop.stockOf(db, 1));
        assertEquals(10, Shop.stockOf(db, 2));
        assertEquals(10, Shop.stockOf(db, 3));
    }

    @Test
    void memoryDisagreesWithTheDatabaseUntilCommit() {
        Database db = Shop.seeded();
        List<Product> products = Shop.products();
        new UnitOfWorkPlacement(db).prepare(Shop.threeLineOrder(), products);
        assertEquals(8, products.get(0).stock());
        assertEquals(10, Shop.stockOf(db, 1));
    }

    @Test
    void theUnitOfWorkHoldsTheLockForTheCommitOnly() {
        Database db = Shop.seeded();
        Order order = Shop.threeLineOrder();
        assertEquals(7, new UnitOfWorkPlacement(db).lockTicks(order));
        assertEquals(22, new TransactionalPlacement(db).lockTicks(order));
    }
}
