package com.jk.explore.servicestub;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", ServiceStubDemo.run());

    @Test
    void real() {
        assertTrue(all.contains("50 test checkouts: £2.50 in lookups, 20 s of waiting"));
        assertTrue(all.contains("no signal: lookup unavailable"));
    }

    @Test
    void stub() {
        assertTrue(all.contains("50 checkouts: 50 lookups, £0.00"));
        assertTrue(all.contains("unknown postcode: postcode not found"));
    }

    @Test
    void contract() {
        assertTrue(all.contains("\"ls1 4ap\": stub says found, real says error"));
    }
}
