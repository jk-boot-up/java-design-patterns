package com.jk.explore.datamapper;

import com.jk.explore.datamapper.domain.Address;
import com.jk.explore.datamapper.domain.Customer;
import com.jk.explore.datamapper.domain.CustomerSummary;
import com.jk.explore.datamapper.pattern.CarelessCustomerMapper;
import com.jk.explore.datamapper.pattern.CustomerMapper;
import com.jk.explore.datamapper.toydb.Database;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

class CustomerMapperTest {

    private final Address address = new Address("12 Mill Lane", "Leeds", "LS1 4AB");
    private final Customer ada = new Customer(1, "Ada", "ada@example.com", address, 10);

    @Test
    void roundTripsEveryFieldAcrossTwoTables() {
        Database db = new Database();
        CustomerMapper mapper = new CustomerMapper(db);
        mapper.insert(ada);

        Customer back = mapper.find(1);
        assertEquals("Ada", back.name());
        assertEquals("ada@example.com", back.email());
        assertEquals(address, back.address());
        assertEquals(10, back.loyaltyPoints());
        assertEquals(1, db.table("customers").size());
        assertEquals(1, db.table("addresses").size());
    }

    @Test
    void oneFindCostsOneSelectPerTable() {
        Database db = new Database();
        CustomerMapper mapper = new CustomerMapper(db);
        mapper.insert(ada);
        db.clearLog();
        mapper.find(1);
        assertEquals(List.of("SELECT customers id=1", "SELECT addresses id=1"), db.operations());
    }

    @Test
    void oneTableFeedsASecondSmallerObject() {
        Database db = new Database();
        CustomerMapper mapper = new CustomerMapper(db);
        mapper.insert(ada);
        assertEquals(List.of(new CustomerSummary(1, "Ada")), mapper.summaries());
    }

    @Test
    void updateChangesTheRowsAndFindSeesIt() {
        Database db = new Database();
        CustomerMapper mapper = new CustomerMapper(db);
        mapper.insert(ada);
        ada.changeEmail("ada@new.example");
        ada.moveTo(new Address("1 High St", "York", "YO1 7HH"));
        mapper.update(ada);
        Customer back = mapper.find(1);
        assertEquals("ada@new.example", back.email());
        assertEquals("York", back.address().city());
    }

    @Test
    void findingAMissingCustomerGivesNull() {
        assertNull(new CustomerMapper(new Database()).find(99));
    }

    @Test
    void aCarelessMappingLosesAFieldWithoutAnyError() {
        Database db = new Database();
        CustomerMapper careless = new CarelessCustomerMapper(db);
        careless.insert(ada);
        Customer back = careless.find(1);
        assertNotNull(back, "every call succeeded");
        assertNull(back.address().postcode(), "the postcode did not round-trip");
        assertNotEquals(ada.address(), back.address());
    }
}
