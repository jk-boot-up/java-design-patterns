package com.jk.explore.inputvalidation;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", InputValidationDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("quantity \"-5\" of a 9.99 mug: total -49.95"));
        assertTrue(all.contains("3 problems:"));
        assertTrue(all.contains("- quantity must be from 1 to 99"));
        assertTrue(all.contains("a good form: accepted, total 19.98"));
        assertTrue(all.contains("new Quantity(-5): quantity must be from 1 to 99"));
        assertTrue(all.contains("Lovely mug &lt;script&gt;"));
        assertTrue(all.contains("REJECTED, a real customer turned away"));
        assertTrue(all.contains("with a rule for letters in any alphabet: accepted"));
    }
}
