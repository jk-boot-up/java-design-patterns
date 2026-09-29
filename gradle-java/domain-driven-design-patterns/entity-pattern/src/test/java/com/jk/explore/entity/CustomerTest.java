package com.jk.explore.entity;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class CustomerTest {

    @Test
    void sameIdIsSameCustomerWhateverTheDetails() {
        Customer a = new Customer(new CustomerId("C-1"), "A", "a@x");
        Customer b = new Customer(new CustomerId("C-1"), "B", "b@x");
        assertEquals(a, b);
        assertEquals(a.hashCode(), b.hashCode());
    }

    @Test
    void differentIdsAreDifferentCustomers() {
        assertNotEquals(new Customer(new CustomerId("C-1"), "A", "a@x"), new Customer(new CustomerId("C-2"), "A", "a@x"));
    }

    @Test
    void changingEmailKeepsIdentityAndRecordsHistory() {
        Customer c = new Customer(new CustomerId("C-1"), "A", "a@x");
        c.changeEmail("b@x");
        assertEquals("C-1", c.id().value());
        assertEquals(2, c.history().size());
    }

    @Test
    void idIsRequired() {
        assertThrows(NullPointerException.class, () -> new Customer(null, "A", "a@x"));
    }

    @Test
    void recordsCompareByValue() {
        assertNotEquals(new CustomerRecord("P", "old", 0), new CustomerRecord("P", "new", 0));
    }
}
