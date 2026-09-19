package com.jk.explore.eda;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class EdaTest {

    @Test
    void directShopLosesTheOrderWhenShippingIsDown() {
        assertFalse(new DirectShop(false).place("ORD-1"));
    }

    @Test
    void orderIsAcceptedWhileAReaderIsDownAndItCatchesUp() {
        EventLog log = new EventLog();
        List<String> seen = new ArrayList<>();
        Reactor r = new Reactor("shipping", false, e -> seen.add(e.orderId()));
        r.goDown();
        new OrderService(log).place("A");
        new OrderService(log).place("B");
        assertEquals(0, r.poll(log));
        assertEquals(2, r.lag(log));
        r.comeUp();
        assertEquals(2, r.poll(log));
        assertEquals(List.of("A", "B"), seen);
        assertEquals(0, r.lag(log));
    }

    @Test
    void aNewReaderSeesHistory() {
        EventLog log = new EventLog();
        new OrderService(log).place("A");
        List<String> seen = new ArrayList<>();
        new Reactor("new", false, e -> seen.add(e.orderId())).poll(log);
        assertEquals(List.of("A"), seen);
    }

    @Test
    void stockIsBehindUntilTheReaderPolls() {
        EventLog log = new EventLog();
        Warehouse w = new Warehouse(10);
        Reactor r = new Reactor("inv", false, w::reserve);
        new OrderService(log).place("A");
        assertEquals(10, w.stock());
        r.poll(log);
        assertEquals(9, w.stock());
    }

    @Test
    void duplicateDeliveryNeedsACheck() {
        EventLog log = new EventLog();
        Warehouse plain = new Warehouse(10);
        Warehouse careful = new Warehouse(10);
        Reactor p = new Reactor("p", false, plain::reserve);
        Reactor c = new Reactor("c", true, careful::reserve);
        new OrderService(log).place("A");
        p.poll(log);
        c.poll(log);
        p.redeliver(log.readFrom(0).get(0));
        c.redeliver(log.readFrom(0).get(0));
        assertEquals(8, plain.stock());
        assertEquals(9, careful.stock());
    }

    @Test
    void rewindReplaysFromTheStart() {
        EventLog log = new EventLog();
        new OrderService(log).place("A");
        List<String> seen = new ArrayList<>();
        Reactor r = new Reactor("r", true, e -> seen.add(e.orderId()));
        r.poll(log);
        r.rewind();
        assertTrue(r.poll(log) == 1);
        assertEquals(2, seen.size());
    }
}
