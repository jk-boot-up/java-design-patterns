package com.jk.explore.datamapper;

import com.jk.explore.datamapper.naive.ActiveRecordCustomer;
import com.jk.explore.datamapper.toydb.Database;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Active Record is shown working, fairly, before its cost is shown. */
class ActiveRecordCustomerTest {

    @Test
    void savesFindsAndUpdatesInOneClassAndThreeOperations() {
        Database db = new Database();
        new ActiveRecordCustomer(db, 1, "Ada", "ada@example.com", "12 Mill Lane", "Leeds", "LS1 4AB").save();
        ActiveRecordCustomer loaded = ActiveRecordCustomer.find(db, 1);
        loaded.changeEmail("ada@new.example");
        loaded.save();

        assertEquals("ada@new.example", ActiveRecordCustomer.find(db, 1).email());
        assertEquals("Leeds", ActiveRecordCustomer.find(db, 1).city());
        assertEquals(3, db.operations().subList(0, 3).size());
        assertEquals("INSERT customers id=1", db.operations().get(0));
        assertEquals("UPDATE customers id=1", db.operations().get(2));
    }
}
