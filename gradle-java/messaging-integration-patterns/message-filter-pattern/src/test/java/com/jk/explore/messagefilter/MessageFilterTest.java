package com.jk.explore.messagefilter;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class MessageFilterTest {

    @Test
    void passesOnlyMatchingMessages() {
        Services.Receiver r = new Services.Receiver();
        MessageFilter f = new MessageFilter("gifts", OrderEvent::gift, r);
        MessageFilterDemo.ORDERS.forEach(f);
        assertEquals(List.of("ORD-2", "ORD-4"), r.received());
        assertEquals(8, f.dropped());
    }

    @Test
    void chainedFiltersApplyBothRules() {
        Services.Receiver r = new Services.Receiver();
        MessageFilter f = new MessageFilter("reg", OrderEvent::registered, new MessageFilter("50", e -> e.pence() > 5000, r));
        MessageFilterDemo.ORDERS.forEach(f);
        assertEquals(List.of("ORD-1", "ORD-4", "ORD-6"), r.received());
    }

    @Test
    void channelDeliversToEverySubscriber() {
        Channel c = new Channel();
        Services.Receiver a = new Services.Receiver();
        Services.Receiver b = new Services.Receiver();
        c.subscribe(a);
        c.subscribe(b);
        c.send(MessageFilterDemo.ORDERS.get(0));
        assertEquals(1, a.received().size());
        assertEquals(1, b.received().size());
    }
}
