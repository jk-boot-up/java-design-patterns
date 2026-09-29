package com.jk.explore.authorization;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", AuthorizationDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("ana views ben's order:   ALLOWED"));
        assertTrue(all.contains("sam refunds 250.00:      ALLOWED"));
        assertTrue(all.contains("ana views ben's order: ALLOW (role CUSTOMER has order:view)"));
        assertTrue(all.contains("ana views ben's order: DENY (no rule allows it)"));
        assertTrue(all.contains("ben views ben's order: ALLOW (owner)"));
        assertTrue(all.contains("sam refunds 80.00:     ALLOW (support, up to 100)"));
        assertTrue(all.contains("sam refunds 250.00:    DENY"));
        assertTrue(all.contains("alex refunds 250.00:   ALLOW (admin)"));
        assertTrue(all.contains("alex exports ben's order: DENY"));
        assertTrue(all.contains("6 decisions logged"));
    }
}
