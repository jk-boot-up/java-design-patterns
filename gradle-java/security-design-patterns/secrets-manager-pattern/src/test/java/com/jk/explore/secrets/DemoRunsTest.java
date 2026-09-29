package com.jk.explore.secrets;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", SecretsManagerDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("is built into 3 services"));
        assertTrue(all.contains("checkout reads it at run time and charges: charged 20.00"));
        assertTrue(all.contains("catalog asks for it: catalog may not read payment-key"));
        assertTrue(all.contains("minute 2, checkout still uses its cached key: pay-key-v1 -> charged 20.00"));
        assertTrue(all.contains("minute 5, the cache refreshes:              pay-key-v2 -> charged 20.00"));
        assertTrue(all.contains("the leaked key, used by an attacker: refused: unknown key"));
        assertTrue(all.contains("holding version 2: refused: unknown key"));
        assertTrue(all.contains("fetches again at once:    pay-key-v3 -> charged 20.00"));
        assertTrue(all.contains("5 reads logged"));
    }
}
