package com.jk.explore.meshenvoy;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import org.junit.jupiter.api.Test;

class MeshEnvoyTest {

    @Test
    void theConfigurationCarriesTheRetriesAndTheCallers() {
        String c = Envoy.configuration(1234, 3, List.of("checkout", "refunds"));
        assertTrue(c.contains("num_retries: 3"));
        assertTrue(c.contains("port_value: 1234"));
        assertTrue(c.contains("exact: checkout") && c.contains("exact: refunds"));
        assertFalse(Envoy.configuration(1234, 3, List.of()).contains("rbac"));
    }

    @Test
    void paymentsRefusesItsFirstCallsOverRealHttp() throws Exception {
        try (Payments p = new Payments()) {
            p.badDay(2);
            String url = "http://127.0.0.1:" + p.port() + "/charge";
            assertEquals(503, new Caller("a", 0).status(url));
            assertEquals(503, new Caller("a", 0).status(url));
            assertEquals(200, new Caller("a", 0).status(url));
            assertEquals(3, p.received());
        }
    }

    @Test
    void theOwnRetryCodeOfEachCallerGivesDifferentResults() throws Exception {
        try (Payments p = new Payments()) {
            String url = "http://127.0.0.1:" + p.port() + "/charge";
            p.badDay(2);
            assertTrue(new Caller("a", 3).call(url));
            p.badDay(2);
            assertFalse(new Caller("b", 0).call(url));
            p.badDay(2);
            assertFalse(new Caller("c", 1).call(url));
        }
    }

    @Test
    void theSixActsRunAgainstARealEnvoy() throws Exception {
        assumeTrue(Envoy.toolsAvailable(), "needs Docker and the Envoy image");
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            MeshEnvoyDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("checkout worked, refunds failed, reports failed"), out);
        assertTrue(out.contains("the call worked. the payment service received 3 calls, and Envoy counts 2 retries"), out);
        assertTrue(out.contains("checkout: status 200. gift-cards: status 403"), out);
        assertTrue(out.contains("the payment service received 3 calls. retrying multiplies"), out);
    }
}
