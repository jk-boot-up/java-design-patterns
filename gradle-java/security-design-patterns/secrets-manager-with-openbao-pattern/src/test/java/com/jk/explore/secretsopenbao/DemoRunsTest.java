package com.jk.explore.secretsopenbao;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;

/** The whole demo against a real OpenBao server; skipped, not failed, without a container runtime. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        assumeTrue(OpenBao.containerRuntimeAvailable(), "needs a container runtime");
        String all = String.join("\n", OpenBaoSecretsDemo.run());
        assertTrue(all.contains("policy \"payments\": HTTP 200, key pay-key-v1"), all);
        assertTrue(all.contains("no such policy:     HTTP 403, permission denied"), all);
        assertTrue(all.contains("written as version 2; checkout now reads: pay-key-v2"), all);
        assertTrue(all.contains("version 1 is kept, for a grace period: pay-key-v1"), all);
        assertTrue(all.contains("used by an attacker: HTTP 403, permission denied"), all);
        assertTrue(all.contains("checkout gets a new token: HTTP 200, key pay-key-v2"), all);
    }

    @Test
    void adviceIsASentenceNotAStackTrace() {
        assertTrue(OpenBao.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
    }
}
