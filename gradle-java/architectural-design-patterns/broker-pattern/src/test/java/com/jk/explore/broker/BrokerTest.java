package com.jk.explore.broker;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.sun.net.httpserver.HttpServer;
import org.junit.jupiter.api.Test;

class BrokerTest {

    @Test
    void forwardsByName() throws Exception {
        HttpServer stock = Services.stock();
        try (Broker b = new Broker()) {
            b.register("stock", Http.url(stock));
            assertEquals("4", Http.get(b.url() + "/call/stock?sku=KETTLE-1"));
        } finally {
            stock.stop(0);
        }
    }

    @Test
    void unknownServiceIsReported() throws Exception {
        try (Broker b = new Broker()) {
            assertTrue(Http.get(b.url() + "/call/nothing?x=1").contains("no service called nothing"));
        }
    }

    @Test
    void takesTurnsBetweenInstances() throws Exception {
        HttpServer a = Services.price("a");
        HttpServer c = Services.price("c");
        try (Broker b = new Broker()) {
            b.addInstance("price", Http.url(a));
            b.addInstance("price", Http.url(c));
            assertTrue(Http.get(b.url() + "/call/price?x=1").contains("from a"));
            assertTrue(Http.get(b.url() + "/call/price?x=1").contains("from c"));
        } finally {
            a.stop(0);
            c.stop(0);
        }
    }
}
