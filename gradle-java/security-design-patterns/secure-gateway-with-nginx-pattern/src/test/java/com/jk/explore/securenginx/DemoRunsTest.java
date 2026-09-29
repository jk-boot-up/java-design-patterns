package com.jk.explore.securenginx;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;

/** The whole demo against a real NGINX container; skipped, not failed, without a container runtime. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        assumeTrue(Gatekeeper.containerRuntimeAvailable(), "needs a container runtime");
        String all = String.join("\n", NginxSecureGatewayDemo.run());
        assertTrue(all.contains("with header X-Internal-Admin=true: 200 export of all 12000 orders"), all);
        assertTrue(all.contains("GET /orders/../admin/export:       200 export of all 12000 orders"), all);
        assertTrue(all.contains("with header X-Internal-Admin=true: 200 order 7"), all);
        assertTrue(all.contains("GET /orders/../admin/export: 404 not found"), all);
        assertTrue(all.contains("DELETE /orders/7:            403 forbidden"), all);
        assertTrue(all.contains("POST /orders:                201 order created"), all);
        assertTrue(all.contains("5 MB body: 413 too large"), all);
        assertTrue(all.contains("GET /orders/7 OR 1=1:    404 not found"), all);
        assertTrue(all.contains("environment holds credentials: false"), all);
    }

    @Test
    void adviceIsASentenceNotAStackTrace() {
        assertTrue(Gatekeeper.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
    }
}
