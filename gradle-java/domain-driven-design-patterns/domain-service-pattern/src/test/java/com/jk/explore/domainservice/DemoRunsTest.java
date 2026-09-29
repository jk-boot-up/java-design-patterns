package com.jk.explore.domainservice;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", DomainServiceDemo.run());

    @Test
    void copiesDisagree() {
        assertTrue(all.contains("web checkout says: £54.00"));
        assertTrue(all.contains("phone app says:    £49.00"));
    }

    @Test
    void serviceAgrees() {
        assertTrue(all.contains("web checkout: £54.00"));
        assertTrue(all.contains("phone app:    £54.00"));
        assertTrue(all.contains("subtotal £60.00; gold 10% -£6.00 beats SAVE5 -£5.00"));
    }

    @Test
    void cases() {
        assertTrue(all.contains("STANDARD, £60.00, SAVE5: £55.00"));
        assertTrue(all.contains("STANDARD, £30.00, SAVE5: £30.00"));
    }
}
