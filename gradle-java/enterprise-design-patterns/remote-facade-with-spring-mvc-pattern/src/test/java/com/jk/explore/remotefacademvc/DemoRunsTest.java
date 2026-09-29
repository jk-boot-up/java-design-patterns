package com.jk.explore.remotefacademvc;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/** The whole demo: a real Spring MVC service on a local port, called over HTTP. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", SpringRemoteFacadeDemo.run());
        assertTrue(all.contains("order screen: 5 round trips, over 0.4 s"), all);
        assertTrue(all.contains("\"customer\":\"Priya\""), all);
        assertTrue(all.contains("order screen: 1 round trip, under 0.2 s"), all);
        assertTrue(all.contains("the order now: 12 High Street, York, Mon 9-12 (new address, old slot)"), all);
        assertTrue(all.contains("facade -> 422 no delivery slot Sun 9-12; the order: 4 Mill Lane, Leeds, Mon 9-12"), all);
        assertTrue(all.contains("facade, a valid slot -> 200 delivery changed; the order: 12 High Street, York, Tue 9-12"), all);
        assertTrue(all.contains("application/problem+json"), all);
        assertTrue(all.contains("8 bytes with the small call, 130 with the summary"), all);
    }
}
