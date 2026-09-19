package com.jk.explore.lazyload;

import com.jk.explore.lazyload.domain.Shop;
import com.jk.explore.lazyload.naive.EagerOrderLoader;
import com.jk.explore.lazyload.pattern.CustomerProxy;
import com.jk.explore.lazyload.pattern.GhostCustomer;
import com.jk.explore.lazyload.pattern.LazyInitOrder;
import com.jk.explore.lazyload.pattern.OrderList;
import com.jk.explore.lazyload.pattern.Session;
import com.jk.explore.lazyload.pattern.SessionClosedException;
import com.jk.explore.lazyload.pattern.ValueHolder;
import com.jk.explore.lazyload.toydb.Database;

import java.util.List;

/** Six acts. Every count comes from the toy database's own operation counter. */
public final class LazyLoadDemo {

    public static void main(String[] args) {
        System.out.println("LAZY LOAD — loading one order, getting everything\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. Eager loading — one order, everything reachable.");
        Database db = Shop.seeded();
        int objects = new EagerOrderLoader(db).load(1);
        System.out.println("  loaded one order. objects created: " + objects);
        System.out.println("  database operations: " + db.operationCount());
        System.out.println("  from a graph with no cycle in it and no obvious mistake.\n");
    }

    private static void actTwo() {
        System.out.println("TWO. Four ways to load later.");
        Database db = Shop.seeded();
        Session session = new Session(db);

        LazyInitOrder init = new LazyInitOrder(session, 1);
        System.out.println("  lazy initialisation: before " + db.operationCount() + ", "
                + describe(db, init::customerName));

        db.clearLog();
        CustomerProxy proxy = new CustomerProxy(session, 2);
        System.out.println("  virtual proxy:       before " + db.operationCount() + ", "
                + describe(db, proxy::name));

        db.clearLog();
        ValueHolder<String> holder = new ValueHolder<>(() -> session.select(Shop.CUSTOMERS, 3).text("name"));
        System.out.println("  value holder:        before " + db.operationCount() + ", "
                + describe(db, holder::value));

        db.clearLog();
        GhostCustomer ghost = new GhostCustomer(session, 4);
        System.out.println("  ghost:               before " + db.operationCount() + ", "
                + describe(db, ghost::name));
        System.out.println("  each costs nothing until first used, and one select then.\n");
    }

    private static String describe(Database db, java.util.function.Supplier<String> use) {
        String name = use.get();
        int afterFirst = db.operationCount();
        use.get();
        return "after first use " + afterFirst + " (" + name + "), after second use " + db.operationCount();
    }

    private static void actThree() {
        System.out.println("THREE. The bill: N+1.");
        Database db = Shop.seeded();
        List<String> page = new OrderList(db).lazy();
        int lazy = db.operationCount();
        db.clearLog();
        new OrderList(db).batched();
        int batched = db.operationCount();
        System.out.println("  a page of " + page.size() + " orders, each showing its customer's name:");
        System.out.println("  lazy:    " + lazy + " queries (one for the orders, one for each customer)");
        System.out.println("  batched: " + batched + " queries");
        System.out.println("  in a real system every query is a round trip, so the lazy page is slower.\n");
    }

    private static void actFour() {
        System.out.println("FOUR. A field access is now I/O, so it can fail.");
        Database db = Shop.seeded();
        CustomerProxy proxy = new CustomerProxy(new Session(db), 1);
        db.failReadNumber(1);
        try {
            proxy.name();
        } catch (IllegalStateException e) {
            System.out.println("  asking for a customer's name threw: " + e.getMessage());
        }
        System.out.println("  it looked like reading a field. it was a database call.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. The session closes first — it fails at the point of use.");
        Database db = Shop.seeded();
        Session session = new Session(db);
        CustomerProxy proxy = new CustomerProxy(session, 1);
        System.out.println("  the object is created while the session is open: no error yet.");
        session.close();
        System.out.println("  the session closes, and the object is passed on to a page.");
        try {
            proxy.name();
        } catch (SessionClosedException e) {
            System.out.println("  the page asks for the name: " + e.getMessage());
        }
        System.out.println("  the failure is where it was used, not where it was created.\n");
    }

    private static void actSix() {
        System.out.println("SIX. Where you have already met this.");
        System.out.println("  that failure has a name in Hibernate: LazyInitializationException.");
        System.out.println("  it is a session-closed exception, exactly as in act five.");
    }
}
