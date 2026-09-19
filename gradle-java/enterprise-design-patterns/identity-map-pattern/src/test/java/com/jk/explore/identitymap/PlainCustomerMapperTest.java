package com.jk.explore.identitymap;

import com.jk.explore.identitymap.domain.Customer;
import com.jk.explore.identitymap.naive.PlainCustomerMapper;
import com.jk.explore.identitymap.toydb.Database;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PlainCustomerMapperTest {

    private PlainCustomerMapper mapper() {
        Database db = CustomerSessionDemo.seeded();
        return new PlainCustomerMapper(db);
    }

    @Test
    void twoLoadsOfTheSameRowGiveTwoObjects() {
        PlainCustomerMapper mapper = mapper();
        assertNotSame(mapper.find(7), mapper.find(7));
        assertNotSame(mapper.findOrder(100).customer(), mapper.find(7));
    }

    @Test
    void theLastWriterWinsAndOneChangeDisappears() {
        Database db = CustomerSessionDemo.seeded();
        PlainCustomerMapper mapper = new PlainCustomerMapper(db);
        Customer a = mapper.find(7);
        Customer b = mapper.find(7);
        a.moveTo("1 High Street, York");
        b.changeEmail("ada@new.example");
        mapper.save(a);
        mapper.save(b);
        assertEquals("12 Mill Lane, Leeds", db.table("customers").peek(7).text("address"));
        assertEquals("ada@new.example", db.table("customers").peek(7).text("email"));
    }

    @Test
    void equalsIsTrueButTheObjectsAreStillSeparatelyChangeable() {
        PlainCustomerMapper mapper = mapper();
        Customer a = mapper.find(7);
        Customer b = mapper.find(7);
        assertEquals(a, b);
        a.moveTo("elsewhere");
        assertTrue(a.equals(b));
        assertEquals("12 Mill Lane, Leeds", b.address());
    }
}
