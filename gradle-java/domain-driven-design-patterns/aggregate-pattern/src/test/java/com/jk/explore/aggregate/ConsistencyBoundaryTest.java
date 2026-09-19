package com.jk.explore.aggregate;

import com.jk.explore.aggregate.domain.*;
import com.jk.explore.aggregate.infrastructure.*;
import com.jk.explore.aggregate.naive.*;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ConsistencyBoundaryTest {

    private static Order order(String id) {
        Order o = new Order(new OrderId(id), new CustomerId("c"));
        o.addLine("A", Money.pounds(1), 1);
        return o;
    }

    @Test
    void theSecondOfTwoSavesOfTheSameOrderIsRefused() {
        VersionedStore<Order> store = new VersionedStore<>(Order::copy);
        store.insert("O", order("O"));
        Loaded<Order> a = store.load("O");
        Loaded<Order> b = store.load("O");
        a.value().addLine("B", Money.pounds(1), 1);
        b.value().addLine("C", Money.pounds(1), 1);
        store.save("O", a);
        assertThrows(ConcurrentModification.class, () -> store.save("O", b));
        assertEquals(2, store.load("O").value().lines().size());
    }

    @Test
    void separateOrdersDoNotConflict() {
        VersionedStore<Order> store = new VersionedStore<>(Order::copy);
        store.insert("O1", order("O1"));
        store.insert("O2", order("O2"));
        Loaded<Order> a = store.load("O1");
        Loaded<Order> b = store.load("O2");
        store.save("O1", a);
        assertDoesNotThrow(() -> store.save("O2", b));
    }

    @Test
    void anAggregateHoldingEveryOrderConflictsOnDifferentOrders() {
        VersionedStore<CustomerWithOrders> store = new VersionedStore<>(CustomerWithOrders::copy);
        CustomerWithOrders c = new CustomerWithOrders();
        c.add(order("O1"));
        c.add(order("O2"));
        store.insert("c", c);
        Loaded<CustomerWithOrders> a = store.load("c");
        Loaded<CustomerWithOrders> b = store.load("c");
        a.value().addLineTo("O1", "X", Money.pounds(1), 1);
        b.value().addLineTo("O2", "Y", Money.pounds(1), 1);
        store.save("c", a);
        assertThrows(ConcurrentModification.class, () -> store.save("c", b));
    }

    @Test
    void aLoadedCopyIsNotTheStoredObject() {
        VersionedStore<Order> store = new VersionedStore<>(Order::copy);
        store.insert("O", order("O"));
        Loaded<Order> loaded = store.load("O");
        loaded.value().addLine("B", Money.pounds(1), 1);
        assertEquals(1, store.load("O").value().lines().size());
    }

    @Test
    void holdingAnIdLoadsNoCustomerButHoldingTheObjectDoes() {
        CustomerRecord.LOADS.set(0);
        new Order(new OrderId("O"), new CustomerId("c"));
        assertEquals(0, CustomerRecord.LOADS.get());
        new EagerOrder(CustomerRecord.load("c"));
        assertEquals(1, CustomerRecord.LOADS.get());
    }

    @Test
    void theLooseOrderAcceptsEverythingTheRootRefuses() {
        LooseOrder o = new LooseOrder();
        o.lines.add(new LooseOrder.Line("A", 100, -3));
        o.placed = true;
        o.lines.add(new LooseOrder.Line("A", 100, 99));
        assertEquals(2, o.lines.size());
    }
}
