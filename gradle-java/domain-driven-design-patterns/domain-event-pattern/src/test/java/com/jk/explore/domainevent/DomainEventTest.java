package com.jk.explore.domainevent;

import com.jk.explore.domainevent.domain.*;
import com.jk.explore.domainevent.infrastructure.Journal;
import com.jk.explore.domainevent.naive.NaivePlaceOrder;
import org.junit.jupiter.api.Test;

import java.lang.reflect.RecordComponent;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class DomainEventTest {

    @Test
    void placingRecordsOneEventAndPullingClearsThem() {
        Order o = new Order("O", "c", 100);
        o.place();
        assertEquals(List.of(new OrderPlaced("O", "c", 100)), o.pullEvents());
        assertEquals(List.of(), o.pullEvents());
    }

    @Test
    void eventsKeepTheOrderTheyHappenedIn() {
        Order o = new Order("O", "c", 100);
        o.place();
        o.cancel("changed my mind");
        assertEquals(List.of(new OrderPlaced("O", "c", 100), new OrderCancelled("O", "changed my mind")), o.pullEvents());
    }

    @Test
    void statesAreGuarded() {
        Order o = new Order("O", "c", 100);
        assertThrows(IllegalStateException.class, () -> o.cancel("x"));
        o.place();
        assertThrows(IllegalStateException.class, o::place);
    }

    @Test
    void anEventCarriesDataAndNeverTheOrderItself() {
        for (Class<?> type : new Class<?>[]{OrderPlaced.class, OrderCancelled.class}) {
            for (RecordComponent c : type.getRecordComponents()) {
                assertNotEquals(Order.class, c.getType());
            }
        }
    }

    @Test
    void theNaiveVersionLeavesAHalfDoneOrderWhenEmailFails() {
        Journal journal = new Journal();
        NaivePlaceOrder naive = new NaivePlaceOrder(journal);
        naive.mailServerDown(true);
        assertThrows(IllegalStateException.class, () -> naive.place("O", "c", 100));
        assertTrue(naive.isSaved("O"));
        assertEquals(1, journal.lines().size());
    }
}
