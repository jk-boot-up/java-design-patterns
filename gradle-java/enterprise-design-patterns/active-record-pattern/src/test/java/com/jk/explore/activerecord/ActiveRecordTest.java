package com.jk.explore.activerecord;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ActiveRecordTest {

    @Test
    void aRecordSavesAndFindsItself() {
        Customer c = new Customer("ada").save();
        Order o = new Order(c.id());
        o.addLine(800, 2);
        o.save();
        Order back = Order.find(o.id());
        assertEquals(1600, back.totalPence());
        assertEquals("DRAFT", back.status());
        assertEquals("ada", Customer.find(c.id()).name());
    }

    @Test
    void savingTwiceUpdatesTheSameRow() {
        Order o = new Order(1).save();
        Integer id = o.id();
        o.addLine(100, 1);
        o.save();
        assertEquals(id, o.id());
        assertEquals(100, Order.find(id).totalPence());
    }

    @Test
    void findersReturnOnlyTheCustomersOrders() {
        Customer a = new Customer("a").save();
        Customer b = new Customer("b").save();
        new Order(a.id()).save();
        new Order(a.id()).save();
        new Order(b.id()).save();
        assertEquals(2, Order.forCustomer(a.id()).size());
        assertEquals(1, Order.forCustomer(b.id()).size());
    }

    @Test
    void rulesLiveOnTheRecord() {
        Order o = new Order(1);
        assertThrows(IllegalStateException.class, o::place);
        o.addLine(100, 1);
        o.place();
        assertThrows(IllegalStateException.class, () -> o.addLine(100, 1));
    }

    @Test
    void aRuleOnTheRecordNeedsTheTableButAPureRuleDoesNot() {
        Customer c = new Customer("cy").save();
        Order o = new Order(c.id());
        o.addLine(3000, 2);
        ActiveRecordDemo.operations();
        Customer.TABLE.resetCount();
        Order.TABLE.resetCount();
        assertTrue(o.qualifiesForFreeDelivery(5000));
        assertEquals(1, ActiveRecordDemo.operations());
        Customer.TABLE.resetCount();
        assertTrue(PureDiscount.qualifiesForFreeDelivery(o.totalPence(), 5000));
        assertEquals(0, ActiveRecordDemo.operations());
    }

    @Test
    void renamingAColumnBreaksLoading() {
        Order o = new Order(1);
        o.addLine(100, 1);
        o.save();
        Order.TABLE.renameColumn("total_pence", "grand_total");
        try {
            assertThrows(IllegalStateException.class, () -> Order.find(o.id()));
        } finally {
            Order.TABLE.renameColumn("grand_total", "total_pence");
        }
    }

    @Test
    void checkingEachOrderLoadsTheCustomerAgain() {
        Customer c = new Customer("di").save();
        for (int i = 0; i < 5; i++) {
            Order o = new Order(c.id());
            o.addLine(3000, 2);
            o.save();
        }
        var orders = Order.forCustomer(c.id());
        Customer.TABLE.resetCount();
        Order.TABLE.resetCount();
        orders.forEach(x -> x.qualifiesForFreeDelivery(5000));
        assertEquals(orders.size(), ActiveRecordDemo.operations());
    }
}
