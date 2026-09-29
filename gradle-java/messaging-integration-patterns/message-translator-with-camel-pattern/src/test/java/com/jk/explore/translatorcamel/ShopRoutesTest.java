package com.jk.explore.translatorcamel;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.apache.camel.CamelContext;
import org.apache.camel.impl.DefaultCamelContext;
import org.junit.jupiter.api.Test;

class ShopRoutesTest {

    @Test
    void formatIsRecognisedFromTheText() {
        assertEquals("json", ShopRoutes.formatOf(" {\"a\":1}"));
        assertEquals("xml", ShopRoutes.formatOf("<order/>"));
        assertEquals("web", ShopRoutes.formatOf("order=1&sku=X"));
        assertEquals("csv", ShopRoutes.formatOf("A,B,1,100"));
    }

    @Test
    void csvPriceInPenceBecomesPounds() throws Exception {
        Warehouse warehouse = new Warehouse();
        try (CamelContext camel = new DefaultCamelContext()) {
            camel.addRoutes(new ShopRoutes(warehouse));
            camel.start();
            camel.createProducerTemplate().sendBody("direct:inbox", "A-1,LAMP-2,3,4500");
        }
        assertEquals("pick 3 x LAMP-2 for A-1", warehouse.picks().get(0));
    }
}
