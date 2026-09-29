package com.jk.explore.tokenspring;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/** The whole demo: real Spring Boot instances on local ports, called over HTTP. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", SpringTokenAuthDemo.run());
        assertTrue(all.contains("next request, to A: 200 ana's cart"), all);
        assertTrue(all.contains("next request, to B: 401 please sign in"), all);
        assertTrue(all.contains("server B: 200 ana's cart  (no shared session store)"), all);
        assertTrue(all.contains("payload changed to ben: 401 Signed JWT rejected: Invalid signature"), all);
        assertTrue(all.contains("expired 2 minutes ago: 401 Jwt expired"), all);
        assertTrue(all.contains("server A: 401 revoked"), all);
        assertTrue(all.contains("server B: 200 ana's cart  (its own list"), all);
        assertTrue(all.contains("signs a token for ben: server A says 200 ben's cart"), all);
    }
}
