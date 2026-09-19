package com.jk.explore.eventbus;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class EventBusTest {

    private final EventBus bus = new EventBus();

    @Test
    void everySubscriberOfATypeHearsThePostedEvent() {
        List<String> got = new ArrayList<>();
        bus.subscribe(OrderPlaced.class, e -> got.add("a" + e.orderId()));
        bus.subscribe(OrderPlaced.class, e -> got.add("b" + e.orderId()));
        bus.post(new OrderPlaced("1", 1));
        assertEquals(List.of("a1", "b1"), got);
    }

    @Test
    void aSubscriberForATypeDoesNotHearOtherTypes() {
        List<String> got = new ArrayList<>();
        bus.subscribe(OrderPlaced.class, e -> got.add(e.orderId()));
        bus.post(new OrderCancelled("1"));
        assertTrue(got.isEmpty());
    }

    @Test
    void aSubscriberForASupertypeHearsAllTheSubtypes() {
        List<String> got = new ArrayList<>();
        bus.subscribe(OrderEvent.class, e -> got.add(e.getClass().getSimpleName()));
        bus.post(new OrderPlaced("1", 1));
        bus.post(new OrderCancelled("1"));
        assertEquals(List.of("OrderPlaced", "OrderCancelled"), got);
    }

    @Test
    void aFailingSubscriberDoesNotStopTheOthersOrTheCaller() {
        List<String> got = new ArrayList<>();
        bus.subscribe(OrderPlaced.class, e -> { throw new IllegalStateException("boom"); });
        bus.subscribe(OrderPlaced.class, e -> got.add("ok"));
        assertDoesNotThrow(() -> bus.post(new OrderPlaced("1", 1)));
        assertEquals(List.of("ok"), got);
        assertEquals(List.of("OrderPlaced: boom"), bus.failures());
    }

    @Test
    void anEventNobodyHearsBecomesADeadEventOnce() {
        List<Object> dead = new ArrayList<>();
        bus.subscribe(DeadEvent.class, d -> dead.add(d.event()));
        bus.post(new OrderPlaced("1", 1));
        assertEquals(1, dead.size());
        assertEquals(1, bus.deadEvents());
    }

    @Test
    void aDeadEventNobodyHearsDoesNotLoopForever() {
        assertDoesNotThrow(() -> bus.post(new OrderPlaced("1", 1)));
        assertEquals(1, bus.deadEvents());
    }

    @Test
    void cancellingRemovesASubscriberAndNotCancellingLeaksIt() {
        var s = bus.subscribe(OrderPlaced.class, e -> { });
        bus.subscribe(OrderPlaced.class, e -> { });
        assertEquals(2, bus.subscribers());
        s.cancel();
        assertEquals(1, bus.subscribers());
    }

    @Test
    void theBusCanBeAskedWhoListensForAType() {
        bus.subscribe(OrderPlaced.class, e -> { });
        bus.subscribe(OrderEvent.class, e -> { });
        bus.subscribe(OrderCancelled.class, e -> { });
        assertEquals(2, bus.subscribersOf(OrderPlaced.class));
    }
}
