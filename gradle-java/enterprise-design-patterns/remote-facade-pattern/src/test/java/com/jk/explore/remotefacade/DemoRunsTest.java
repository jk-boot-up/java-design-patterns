package com.jk.explore.remotefacade;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", RemoteFacadeDemo.run());
    }

    @Test
    void fineGrained() {
        assertTrue(all.contains("order screen: 5 round trips, 400 ms"));
    }

    @Test
    void facade() {
        assertTrue(all.contains("order screen: 1 round trip, 80 ms"));
    }

    @Test
    void allOrNothing() {
        assertTrue(all.contains("new address, old slot: 12 High Street, York, Mon 9-12"));
        assertTrue(all.contains("the order is unchanged: 4 Mill Lane, Leeds, Mon 9-12"));
        assertTrue(all.contains("the order now: 12 High Street, York, Tue 9-12"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("8 bytes with the small call, 73 with the summary"));
    }
}
