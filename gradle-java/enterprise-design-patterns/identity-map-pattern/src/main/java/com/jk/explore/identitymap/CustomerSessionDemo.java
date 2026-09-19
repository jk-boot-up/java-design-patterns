package com.jk.explore.identitymap;

import com.jk.explore.identitymap.domain.Customer;
import com.jk.explore.identitymap.domain.Order;
import com.jk.explore.identitymap.naive.PlainCustomerMapper;
import com.jk.explore.identitymap.pattern.CustomerSession;
import com.jk.explore.identitymap.toydb.Database;
import com.jk.explore.identitymap.toydb.Row;

/** Six acts. Every count comes from the toy database's own operation counter. */
public final class CustomerSessionDemo {

    static Database seeded() {
        Database db = new Database();
        PlainCustomerMapper mapper = new PlainCustomerMapper(db);
        mapper.insert(new Customer(7, "Ada Lovelace", "ada@example.com", "12 Mill Lane, Leeds"));
        mapper.insertOrder(100, 7);
        db.clearLog();
        return db;
    }

    public static void main(String[] args) {
        System.out.println("IDENTITY MAP — the same customer, twice\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. Two loads, two objects.");
        Database db = seeded();
        PlainCustomerMapper mapper = new PlainCustomerMapper(db);
        Order order = mapper.findOrder(100);
        Customer direct = mapper.find(7);
        System.out.println("  the order's customer, and customer 7 loaded by id:");
        System.out.println("  same object (==): " + (order.customer() == direct));
        System.out.println("  " + db.operationCount() + " selects: the order, its customer, and the same customer again.\n");
    }

    private static void actTwo() {
        System.out.println("TWO. The lost change.");
        Database db = seeded();
        PlainCustomerMapper mapper = new PlainCustomerMapper(db);
        Customer viaOrder = mapper.findOrder(100).customer();
        Customer direct = mapper.find(7);
        viaOrder.moveTo("1 High Street, York");
        direct.changeEmail("ada@newmail.example");
        mapper.save(viaOrder);
        mapper.save(direct);
        Row stored = db.table("customers").peek(7);
        System.out.println("  one object moved her to York. the other changed her email. both saved.");
        System.out.println("  stored address: " + stored.text("address"));
        System.out.println("  stored email:   " + stored.text("email"));
        System.out.println("  the address change silently disappeared: last writer wins.\n");
    }

    private static void actThree() {
        System.out.println("THREE. equals() is not enough.");
        Database db = seeded();
        PlainCustomerMapper mapper = new PlainCustomerMapper(db);
        Customer a = mapper.find(7);
        Customer b = mapper.find(7);
        a.moveTo("1 High Street, York");
        System.out.println("  equals: " + a.equals(b) + ", same object: " + (a == b));
        System.out.println("  one moved to " + a.address() + ", the other still says " + b.address());
        System.out.println("  equal, and still separately changeable.\n");
    }

    private static void actFour() {
        System.out.println("FOUR. The pattern — one map, one object.");
        Database db = seeded();
        CustomerSession session = new CustomerSession(db);
        Order order = session.findOrder(100);
        Customer direct = session.find(7);
        System.out.println("  the order's customer and customer 7 by id, same object (==): "
                + (order.customer() == direct));
        System.out.println("  " + db.operationCount() + " selects: the order's row, and the customer once.");
        db.clearLog();
        session.find(7);
        session.find(7);
        System.out.println("  two more finds of customer 7 cost " + db.operationCount() + " operations.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. The map is a cache, so it can be stale.");
        Database db = seeded();
        CustomerSession session = new CustomerSession(db);
        Customer seen = session.find(7);
        db.table("customers").update(7, Row.of("name", "Ada Lovelace", "email", "ada@other.example",
                "address", "12 Mill Lane, Leeds"));
        System.out.println("  another process changed the email in the database.");
        System.out.println("  this session still sees: " + session.find(7).email());
        System.out.println("  a new session sees:      " + new CustomerSession(db).find(7).email());
        System.out.println("  same object still: " + (seen == session.find(7)) + "\n");
    }

    private static void actSix() {
        System.out.println("SIX. It holds references, and its scope is a decision.");
        Database db = new Database();
        PlainCustomerMapper plain = new PlainCustomerMapper(db);
        for (int i = 1; i <= 1_000; i++) {
            plain.insert(new Customer(i, "Customer " + i, "c" + i + "@example.com", "Somewhere " + i));
        }
        CustomerSession session = new CustomerSession(db);
        for (int i = 1; i <= 1_000; i++) {
            session.find(i);
        }
        System.out.println("  a bulk load of 1000 customers: the session now holds " + session.loadedCount() + " objects.");
        System.out.println("  per request, per session, or per application: each is wrong in a different way.");
        System.out.println("  where you have met this: the JPA persistence context is an identity map.");
    }
}
