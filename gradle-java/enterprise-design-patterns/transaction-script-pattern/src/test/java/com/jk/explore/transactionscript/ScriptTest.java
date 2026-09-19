package com.jk.explore.transactionscript;

import com.jk.explore.transactionscript.script.*;
import org.junit.jupiter.api.Test;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

class ScriptTest {

    @Test
    void aScriptPlacesAnOrderAndTakesStock() {
        Db db = new Db();
        Db.SavedOrder o = new PlaceOrderScript(db, new Payment()).run("ada", "MUG-BLUE", 2);
        assertEquals(1600, o.totalPence());
        assertEquals(8, db.stockOf("MUG-BLUE"));
        assertEquals(1, db.orders().size());
    }

    @Test
    void aFailureAfterTheStockWasTakenUndoesEverything() {
        Db db = new Db();
        Payment p = new Payment();
        p.declineNext();
        assertThrows(IllegalStateException.class, () -> new PlaceOrderScript(db, p).run("ada", "MUG-BLUE", 2));
        assertEquals(10, db.stockOf("MUG-BLUE"));
        assertEquals(0, db.orders().size());
    }

    @Test
    void validationRefusesBeforeAnythingChanges() {
        Db db = new Db();
        PlaceOrderScript s = new PlaceOrderScript(db, new Payment());
        assertThrows(IllegalArgumentException.class, () -> s.run("a", "MUG-BLUE", 0));
        assertThrows(IllegalStateException.class, () -> s.run("a", "ESP-001", 4));
        assertEquals(3, db.stockOf("ESP-001"));
    }

    @Test
    void theCopiedPricingDrifts() {
        Db db = new Db();
        Db.SavedOrder o = new PlaceOrderScript(db, new Payment()).run("ada", "MUG-BLUE", 7);
        long amended = new AmendOrderScript(db).run(o.id(), "MUG-BLUE", 7);
        assertEquals(5040, o.totalPence());
        assertEquals(5600, amended);
    }

    @Test
    void theSharedHelperAgreesWithThePlacedOrder() {
        assertEquals(5040, Pricing.total("MUG-BLUE", 7));
        assertEquals(800 * 4, Pricing.total("MUG-BLUE", 4));
    }

    @Test
    void theGrownScriptAppliesEveryRule() {
        Db db = new Db();
        PlaceOrderScriptGrown s = new PlaceOrderScriptGrown(db, new Payment());
        Db.SavedOrder o = s.run("ada", "MUG-BLUE", 2, true, "EU", "SAVE5");
        assertEquals(1324, o.totalPence());
    }

    @Test
    void decisionsAndPathsGrow() throws IOException {
        assertEquals(3, TransactionScriptDemo.branches("PlaceOrderScript.java"));
        assertEquals(7, TransactionScriptDemo.branches("PlaceOrderScriptGrown.java"));
    }

    @Test
    void theMonthEndScriptSumsTheOrders() {
        Db db = new Db();
        PlaceOrderScript s = new PlaceOrderScript(db, new Payment());
        s.run("ada", "MUG-BLUE", 2);
        s.run("ben", "ESP-001", 1);
        assertEquals("2 orders, £316.00 taken", MonthEndScript.run(db));
    }
}
