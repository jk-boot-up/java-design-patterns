package com.jk.explore.domainevent;

import com.jk.explore.domainevent.domain.Order;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class RelayTest {

    private static Order placed(String id) {
        Order o = new Order(id, "ada", 4999);
        o.place();
        return o;
    }

    @Test
    void nothingIsDeliveredUntilTheRelayRuns() {
        var shop = new DomainEventDemo.Shop();
        shop.orders.save(placed("O"));
        assertEquals(1, shop.orders.pending());
        assertEquals(0, shop.journal.lines().size());
        assertEquals(java.util.List.of(), shop.orders.relay());
        assertEquals(3, shop.journal.lines().size());
        assertEquals(0, shop.orders.pending());
    }

    @Test
    void aFailingHandlerDoesNotStopTheOthersAndIsRetriedAlone() {
        var shop = new DomainEventDemo.Shop();
        shop.email.mailServerDown(true);
        shop.orders.save(placed("O"));
        assertEquals(1, shop.orders.relay().size());
        assertEquals(2, shop.journal.lines().size());
        assertEquals(1, shop.orders.pending());
        shop.email.mailServerDown(false);
        assertEquals(0, shop.orders.relay().size());
        assertEquals(3, shop.journal.lines().size());
        assertEquals(0, shop.orders.pending());
    }

    @Test
    void relayingTwiceDeliversOnce() {
        var shop = new DomainEventDemo.Shop();
        shop.orders.save(placed("O"));
        shop.orders.relay();
        shop.orders.relay();
        assertEquals(3, shop.journal.lines().size());
    }

    @Test
    void eventsSavedWithTheOrderSurviveAMissedRelay() {
        var shop = new DomainEventDemo.Shop();
        shop.orders.save(placed("O"));
        assertEquals(1, shop.orders.pending());
        shop.orders.relay();
        assertEquals(3, shop.journal.lines().size());
    }

    @Test
    void severalOrdersAreDeliveredInTheOrderTheyWereSaved() {
        var shop = new DomainEventDemo.Shop();
        shop.orders.save(placed("A"));
        shop.orders.save(placed("B"));
        shop.orders.relay();
        var stock = shop.journal.lines().stream().filter(l -> l.startsWith("stock")).toList();
        assertEquals(java.util.List.of("stock: reserved for A", "stock: reserved for B"), stock);
    }
}
