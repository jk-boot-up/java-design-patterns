package com.jk.explore.authzspring;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/** The whole demo: a real Spring Boot server on a local port, called over HTTP as four users. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", SpringAuthorizationDemo.run());
        assertTrue(all.contains("ana views ben's order ORD-7: 200 order ORD-7"), all);
        assertTrue(all.contains("ana views ORD-7 (ben's):   403 forbidden"), all);
        assertTrue(all.contains("ben views ORD-7 (ben's own): 200 order ORD-7"), all);
        assertTrue(all.contains("sam (support) refunds 80:  200 refunded 80.0"), all);
        assertTrue(all.contains("sam (support) refunds 250: 403 forbidden"), all);
        assertTrue(all.contains("alex (admin) refunds 250:  200 refunded 250.0"), all);
        assertTrue(all.contains("an endpoint no rule mentions: 403 forbidden"), all);
        assertTrue(all.contains("announced as events: 3"), all);
    }
}
