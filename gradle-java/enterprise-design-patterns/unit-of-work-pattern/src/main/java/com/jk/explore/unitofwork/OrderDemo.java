package com.jk.explore.unitofwork;

import com.jk.explore.unitofwork.domain.Order;
import com.jk.explore.unitofwork.domain.Product;
import com.jk.explore.unitofwork.domain.Shop;
import com.jk.explore.unitofwork.naive.SelfSavingPlacement;
import com.jk.explore.unitofwork.naive.TransactionalPlacement;
import com.jk.explore.unitofwork.pattern.UnitOfWork;
import com.jk.explore.unitofwork.pattern.UnitOfWorkPlacement;
import com.jk.explore.unitofwork.toydb.Database;

import java.util.List;

/**
 * Six acts. One scenario throughout: an order with three lines, where the
 * write that decrements the third product's stock is rejected.
 */
public final class OrderDemo {

    /** Order row, then per line: stock update, line row. The sixth write is the third stock update. */
    static final int THIRD_STOCK_UPDATE = 6;

    /** In commit order: order, three lines, then three stock updates. The seventh write is the third stock update. */
    static final int THIRD_STOCK_UPDATE_AT_COMMIT = 7;

    public static void main(String[] args) {
        System.out.println("UNIT OF WORK — save half an order\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static String stockLine(Database db) {
        return "keyboard " + Shop.stockOf(db, 1) + ", mouse " + Shop.stockOf(db, 2) + ", monitor " + Shop.stockOf(db, 3);
    }

    private static void actOne() {
        System.out.println("ONE. Each object saves itself — the wreckage.");
        Database db = Shop.seeded();
        db.failWriteNumber(THIRD_STOCK_UPDATE);
        Order order = Shop.threeLineOrder();
        try {
            new SelfSavingPlacement(db).place(order, Shop.products());
        } catch (IllegalStateException e) {
            System.out.println("  the third stock update failed: " + e.getMessage());
        }
        System.out.println("  orders in the database:      " + db.table(Shop.ORDERS).size());
        System.out.println("  order lines in the database: " + db.table(Shop.LINES).size() + " of 3");
        System.out.println("  stock now: " + stockLine(db) + " (was 10, 10, 10)");
        System.out.println("  nothing knows it is broken, and nothing can undo it.\n");
    }

    private static void actTwo() {
        System.out.println("TWO. Wrap it in a transaction — it mostly works.");
        Database db = Shop.seeded();
        db.failWriteNumber(THIRD_STOCK_UPDATE);
        Order order = Shop.threeLineOrder();
        TransactionalPlacement placement = new TransactionalPlacement(db);
        try {
            placement.place(order, Shop.products());
        } catch (IllegalStateException e) {
            System.out.println("  the third stock update failed, and the transaction rolled back.");
        }
        System.out.println("  orders: " + db.table(Shop.ORDERS).size() + ", lines: " + db.table(Shop.LINES).size()
                + ", stock: " + stockLine(db));
        System.out.println("  the cost: the transaction was open for " + placement.lockTicks(order)
                + " ticks, including every slow check.\n");
    }

    private static void actThree() {
        System.out.println("THREE. The pattern — nothing touches the database until commit.");
        Database db = Shop.seeded();
        Order order = Shop.threeLineOrder();
        UnitOfWorkPlacement placement = new UnitOfWorkPlacement(db);
        UnitOfWork work = placement.prepare(order, Shop.products());
        System.out.println("  after changing every object: " + db.operationCount() + " database operations, "
                + work.pendingChanges() + " changes registered.");
        work.commit();
        System.out.println("  commit wrote them, parents first:");
        db.operations().forEach(op -> System.out.println("    " + op));
        System.out.println("  the database was locked for " + placement.lockTicks(order) + " ticks, not "
                + new TransactionalPlacement(db).lockTicks(order) + ".\n");
    }

    private static void actFour() {
        System.out.println("FOUR. The same failure, through a unit of work.");
        Database db = Shop.seeded();
        db.failWriteNumber(THIRD_STOCK_UPDATE_AT_COMMIT);
        UnitOfWork work = new UnitOfWorkPlacement(db).prepare(Shop.threeLineOrder(), Shop.products());
        try {
            work.commit();
        } catch (IllegalStateException e) {
            System.out.println("  commit failed: " + e.getMessage());
        }
        System.out.println("  orders: " + db.table(Shop.ORDERS).size() + ", lines: " + db.table(Shop.LINES).size()
                + ", stock: " + stockLine(db));
        System.out.println("  all of the order, or none of it.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. The bill — order of writes matters.");
        Database db = Shop.seeded();
        Order order = Shop.threeLineOrder();
        UnitOfWork work = new UnitOfWorkPlacement(db).prepare(order, Shop.products());
        try {
            work.commitInRegistrationOrder();
        } catch (IllegalStateException e) {
            System.out.println("  written in the order registered, the lines came before their order:");
            System.out.println("  " + e.getMessage());
        }
        Database db2 = Shop.seeded();
        UnitOfWork sorted = new UnitOfWorkPlacement(db2).prepare(Shop.threeLineOrder(), Shop.products());
        sorted.commit();
        System.out.println("  the unit of work sorts them: the order first. orders: " + db2.table(Shop.ORDERS).size() + ".\n");
    }

    private static void actSix() {
        System.out.println("SIX. Memory disagrees with the database until commit.");
        Database db = Shop.seeded();
        List<Product> products = Shop.products();
        UnitOfWork work = new UnitOfWorkPlacement(db).prepare(Shop.threeLineOrder(), products);
        System.out.println("  in memory, the keyboard has " + products.get(0).stock() + " in stock.");
        System.out.println("  in the database, it still has " + Shop.stockOf(db, 1) + ".");
        System.out.println("  the change set lives in memory: " + work.pendingChanges() + " changes for one order.");
        work.commit();
        System.out.println("  where you have met this: @Transactional is a unit of work, and a flush is its commit.");
    }
}
