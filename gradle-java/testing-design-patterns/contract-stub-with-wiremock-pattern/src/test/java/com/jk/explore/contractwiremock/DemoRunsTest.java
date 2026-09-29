package com.jk.explore.contractwiremock;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/** The whole demo: real WireMock stubs and a real payment service on local ports. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", WireMockContractStubDemo.run());
        assertTrue(all.contains("hand-written WireMock stub: order confirmed"), all);
        assertTrue(all.contains("payment service version 2: order stuck: no result in the reply"), all);
        assertTrue(all.contains("lists 3 interactions"), all);
        assertTrue(all.contains("card, no funds: card declined: insufficient funds"), all);
        assertTrue(all.contains("version 1: 3 of 3 interactions match"), all);
        assertTrue(all.contains("version 2: 0 of 3 match"), all);
        assertTrue(all.contains("hand-written stub, charge in USD: order confirmed"), all);
        assertTrue(all.contains("contract stub, charge in USD:    404 from the stub: Request was not matched"), all);
    }
}
