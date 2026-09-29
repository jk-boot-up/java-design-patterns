package com.jk.explore.pageobject;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", PageObjectDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("click #apply-btn, read #total: 50.00"));
        assertTrue(all.contains("name the selector themselves: 0 of 5 pass"));
        assertTrue(all.contains("after one selector is changed in it: 5 of 5 pass"));
        assertTrue(all.contains("checkout.applyCoupon(\"SAVE10\").total(): 45.00"));
        assertTrue(all.contains("ConfirmationPage: ORD-1042, \"Thank you for your order\""));
    }
}
