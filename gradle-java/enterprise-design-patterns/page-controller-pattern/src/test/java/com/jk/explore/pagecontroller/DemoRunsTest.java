package com.jk.explore.pagecontroller;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", PageControllerDemo.run());
    }

    @Test
    void oneHandlerBreaksTheProductPage() {
        assertTrue(all.contains("GET /product?sku=KETTLE-1      -> 500 server error: NumberFormatException"));
    }

    @Test
    void controllers() {
        assertTrue(all.contains("-> 200 steel kettle, £30.00"));
        assertTrue(all.contains("-> 404 no product SOFA-9"));
        assertTrue(all.contains("-> 400 quantity must be a number"));
        assertTrue(all.contains("-> 200 reviews for KETTLE-1: 4.5 stars from 12 customers"));
    }

    @Test
    void forgottenCheck() {
        assertTrue(all.contains("not logged in      -> 401 please log in"));
        assertTrue(all.contains("not logged in    -> 200 checkout: pay £63.44"));
    }
}
