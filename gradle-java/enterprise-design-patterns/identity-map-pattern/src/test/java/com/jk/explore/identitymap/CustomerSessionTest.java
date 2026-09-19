package com.jk.explore.identitymap;

import com.jk.explore.identitymap.domain.Customer;
import com.jk.explore.identitymap.naive.PlainCustomerMapper;
import com.jk.explore.identitymap.pattern.CustomerSession;
import com.jk.explore.identitymap.toydb.Database;
import com.jk.explore.identitymap.toydb.Row;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertSame;

class CustomerSessionTest {

    @Test
    void anOrdersCustomerAndACustomerLoadedByIdAreTheSameObject() {
        CustomerSession session = new CustomerSession(CustomerSessionDemo.seeded());
        assertSame(session.findOrder(100).customer(), session.find(7));
    }

    @Test
    void aSecondFindCostsNoOperationAtAll() {
        Database db = CustomerSessionDemo.seeded();
        CustomerSession session = new CustomerSession(db);
        session.find(7);
        db.clearLog();
        session.find(7);
        session.find(7);
        assertEquals(0, db.operationCount());
    }

    @Test
    void oneObjectMeansTheSecondChangeCannotOverwriteTheFirst() {
        Database db = CustomerSessionDemo.seeded();
        CustomerSession session = new CustomerSession(db);
        Customer a = session.find(7);
        Customer b = session.find(7);
        a.moveTo("1 High Street, York");
        b.changeEmail("ada@new.example");
        session.save(b);
        assertEquals("1 High Street, York", db.table("customers").peek(7).text("address"));
        assertEquals("ada@new.example", db.table("customers").peek(7).text("email"));
    }

    @Test
    void theSessionIsAStaleCacheAndANewSessionIsFresh() {
        Database db = CustomerSessionDemo.seeded();
        CustomerSession session = new CustomerSession(db);
        Customer seen = session.find(7);
        db.table("customers").update(7, Row.of("name", "Ada Lovelace", "email", "ada@other.example",
                "address", "12 Mill Lane, Leeds"));
        assertEquals("ada@example.com", session.find(7).email());
        assertEquals("ada@other.example", new CustomerSession(db).find(7).email());
        assertNotSame(seen, new CustomerSession(db).find(7));
    }

    @Test
    void aBulkLoadMakesTheSessionHoldEveryObject() {
        Database db = new Database();
        PlainCustomerMapper plain = new PlainCustomerMapper(db);
        for (int i = 1; i <= 500; i++) {
            plain.insert(new Customer(i, "c" + i, "e", "a"));
        }
        CustomerSession session = new CustomerSession(db);
        for (int i = 1; i <= 500; i++) {
            session.find(i);
        }
        assertEquals(500, session.loadedCount());
    }
}
