package com.jk.explore.filtercamel;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.apache.camel.CamelContext;
import org.apache.camel.impl.DefaultCamelContext;
import org.junit.jupiter.api.Test;

class ShopRoutesTest {

    @Test
    void guestsNeverReachLoyaltyWhateverTheAmount() throws Exception {
        Received loyalty = new Received();
        Received discard = new Received();
        try (CamelContext camel = new DefaultCamelContext()) {
            camel.addRoutes(new ShopRoutes(new Received(), loyalty, discard, new Rules(), true));
            camel.start();
            camel.createProducerTemplate().sendBody("direct:loyalty", new OrderEvent("G", false, 99999, false));
        }
        assertEquals(List.of(), loyalty.orders());
        assertEquals(List.of("G"), discard.orders());
    }

    @Test
    void thresholdIsStrictlyGreater() throws Exception {
        Received loyalty = new Received();
        try (CamelContext camel = new DefaultCamelContext()) {
            camel.addRoutes(new ShopRoutes(new Received(), loyalty, new Received(), new Rules(), true));
            camel.start();
            camel.createProducerTemplate().sendBody("direct:loyalty", new OrderEvent("E", true, 5000, false));
        }
        assertEquals(List.of(), loyalty.orders());
    }
}
