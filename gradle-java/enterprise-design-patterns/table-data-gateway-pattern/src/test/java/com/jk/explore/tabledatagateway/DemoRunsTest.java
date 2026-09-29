package com.jk.explore.tabledatagateway;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", TableDataGatewayDemo.run());
    }

    @Test
    void scatteredBreaks() {
        assertTrue(all.contains("product page: FAILED, Column \"STOCK\" not found"));
        assertTrue(all.contains("checkout:     FAILED, Column \"STOCK\" not found"));
    }

    @Test
    void gatewayWorks() {
        assertTrue(all.contains("cheaper than £10: [tea towel, mug]"));
        assertTrue(all.contains("checkout took 1 kettle: steel kettle, 2 in stock"));
    }

    @Test
    void sqlLivesInOnePlace() {
        assertTrue(all.contains("old way: 3"));
        assertTrue(all.contains("new way: 0; the gateway: 1 class"));
    }
}
