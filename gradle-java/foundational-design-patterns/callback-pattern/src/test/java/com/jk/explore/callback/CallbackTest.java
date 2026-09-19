package com.jk.explore.callback;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class CallbackTest {

    @Test
    void waitingCostsLooks() {
        WaitingGateway.Handle h = new WaitingGateway().charge("A", 5);
        while (!h.isDone()) {
            // wait
        }
        assertEquals(5, h.polls());
    }

    @Test
    void theCallbackRunsWhenTheAnswerComesNotBefore() {
        Gateway g = new Gateway();
        List<String> log = new ArrayList<>();
        g.charge("A", r -> log.add("callback " + r.message()));
        log.add("caller goes on");
        assertEquals(List.of("caller goes on"), log);
        g.complete("A", true);
        assertEquals(List.of("caller goes on", "callback paid"), log);
        assertEquals(0, g.pending());
    }

    @Test
    void theResultTellsTheCallbackWhatHappened() {
        Gateway g = new Gateway();
        List<Boolean> seen = new ArrayList<>();
        g.charge("A", r -> seen.add(r.paid()));
        g.complete("A", false);
        assertEquals(List.of(false), seen);
    }

    @Test
    void aFailingCallbackDoesNotStopTheGateway() {
        Gateway g = new Gateway();
        List<String> log = new ArrayList<>();
        g.charge("A", r -> {
            throw new IllegalStateException("boom");
        });
        g.charge("B", r -> log.add(r.orderId()));
        g.complete("A", true);
        g.complete("B", true);
        assertEquals(List.of("B"), log);
        assertEquals(List.of("A: boom"), g.callbackErrors());
    }

    @Test
    void aSharedFieldMixesOrdersUpButACapturedIdDoesNot() {
        Gateway g = new Gateway();
        SharedFieldShop shop = new SharedFieldShop(g);
        shop.pay("A");
        shop.pay("B");
        g.complete("A", true);
        g.complete("B", true);
        assertEquals(List.of("B paid", "B paid"), shop.log());
    }

    @Test
    void nestedCallbacksRunOutsideTheirWrittenOrder() {
        Gateway first = new Gateway();
        Gateway second = new Gateway();
        List<String> log = new ArrayList<>();
        first.charge("A", r -> {
            log.add("first done");
            second.charge("A", s -> log.add("second done"));
            log.add("second asked");
        });
        log.add("start");
        first.complete("A", true);
        assertTrue(log.indexOf("second asked") < log.size());
        second.complete("A", true);
        assertEquals(List.of("start", "first done", "second asked", "second done"), log);
    }
}
