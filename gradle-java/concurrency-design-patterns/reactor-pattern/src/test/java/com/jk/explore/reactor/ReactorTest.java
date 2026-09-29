package com.jk.explore.reactor;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class ReactorTest {

    @Test
    void answersOverTheNetwork() throws Exception {
        try (Reactor r = new Reactor(); Clients c = new Clients(r.port(), 3)) {
            assertEquals("4", c.ask(0, "stock KETTLE-1"));
            assertEquals("800", c.ask(1, "price MUG-1"));
            assertEquals("unknown command", c.ask(2, "hello"));
        }
    }

    @Test
    void oneThreadServesManyClients() throws Exception {
        try (Reactor r = new Reactor(); Clients c = new Clients(r.port(), 50)) {
            for (int i = 0; i < 50; i++) {
                c.send(i, "stock MUG-1");
            }
            for (int i = 0; i < 50; i++) {
                assertEquals("20", c.read(i));
            }
            assertEquals(1, r.handlerThreads());
        }
    }

    @Test
    void commandsWithoutNetwork() {
        assertEquals("20", StockCommands.answer("stock MUG-1"));
        assertEquals("0", StockCommands.answer("stock NOPE"));
    }
}
