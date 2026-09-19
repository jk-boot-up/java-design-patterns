package com.jk.explore.messagechannel;

import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class MessageChannelTest {

    private static Message<String> m(String id) {
        return Message.of(id, "PickOrder", "ORD-" + id);
    }

    @Test
    void aDirectCallFailsWhileTheOtherSystemIsDown() {
        Warehouse w = new Warehouse();
        w.goDown();
        assertThrows(IllegalStateException.class, () -> w.pick("A"));
    }

    @Test
    void aChannelAcceptsMessagesWhileTheReceiverIsDownAndDeliversThemInOrderLater() {
        Channel<String> c = new Channel<>("c", "PickOrder", 10);
        Warehouse w = new Warehouse();
        w.goDown();
        c.send(m("1"));
        c.send(m("2"));
        c.send(m("3"));
        assertEquals(3, c.waiting());
        w.comeBack();
        for (Message<String> x = c.receive(); x != null; x = c.receive()) w.pick(x.body());
        assertEquals(java.util.List.of("ORD-1", "ORD-2", "ORD-3"), w.told());
    }

    @Test
    void eachMessageIsTakenByOneReceiverOnce() {
        Channel<String> c = new Channel<>("c", "PickOrder", 10);
        c.send(m("1"));
        assertNotNull(c.receive());
        assertNull(c.receive());
        assertEquals(1, c.sent());
        assertEquals(1, c.received());
    }

    @Test
    void anEnvelopeCarriesHeadersApartFromTheBody() {
        Message<String> x = new Message<>("1", "PickOrder", Map.of("priority", "express"), "body");
        assertEquals("express", x.headers().get("priority"));
        assertEquals("body", x.body());
    }

    @Test
    void aChannelRefusesTheWrongTypeOfMessage() {
        Channel<String> c = new Channel<>("c", "PickOrder", 10);
        assertThrows(WrongType.class, () -> c.send(Message.of("1", "RefundRequest", "x")));
        assertEquals(0, c.waiting());
    }

    @Test
    void aFullChannelRefusesAndNothingIsLost() {
        Channel<String> c = new Channel<>("c", "PickOrder", 2);
        c.send(m("1"));
        c.send(m("2"));
        assertThrows(ChannelFull.class, () -> c.send(m("3")));
        assertEquals(2, c.waiting());
        assertEquals(2, c.sent());
    }
}
