package com.jk.explore.datamapper;

import com.jk.explore.datamapper.domain.Address;
import com.jk.explore.datamapper.domain.Customer;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Field;
import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;

/** The domain object is tested with no database anywhere in the test. */
class CustomerTest {

    private final Customer ada = new Customer(1, "Ada", "ada@example.com",
            new Address("12 Mill Lane", "Leeds", "LS1 4AB"), 0);

    @Test
    void rejectsAnEmailWithNoAtSign() {
        assertThrows(IllegalArgumentException.class, () -> ada.changeEmail("nonsense"));
    }

    @Test
    void earnsPoints() {
        ada.earnPoints(5);
        assertEquals(5, ada.loyaltyPoints());
    }

    @Test
    void holdsNoPersistenceStateOfAnyKind() {
        for (Field f : Customer.class.getDeclaredFields()) {
            String type = f.getType().getName();
            assertFalse(type.contains("toydb"), "field " + f.getName() + " references the database");
        }
        assertFalse(Arrays.stream(Customer.class.getDeclaredMethods())
                .anyMatch(m -> m.getName().equals("save") || m.getName().equals("find")));
    }
}
