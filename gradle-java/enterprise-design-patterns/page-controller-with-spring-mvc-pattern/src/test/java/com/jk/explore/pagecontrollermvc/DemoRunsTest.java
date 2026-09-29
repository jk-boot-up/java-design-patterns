package com.jk.explore.pagecontrollermvc;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/** The whole demo: a real Spring MVC application on a local port, called over HTTP. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", SpringPageControllerDemo.run());
        assertTrue(all.contains("GET /old/product?sku=KETTLE-1   -> 500"), all);
        assertTrue(all.contains("GET /product?sku=KETTLE-1       -> 200 steel kettle, £30.00"), all);
        assertTrue(all.contains("GET /product?sku=SOFA-9         -> 404"), all);
        assertTrue(all.contains("GET /basket?add=MUG-1&qty=two   -> 400"), all);
        assertTrue(all.contains("-> 200 reviews for KETTLE-1"), all);
        assertTrue(all.contains("not logged in    -> 200 checkout"), all);
        assertTrue(all.contains("not logged in    -> 401 please log in"), all);
        assertTrue(all.contains("logged in        -> 200 checkout"), all);
    }
}
