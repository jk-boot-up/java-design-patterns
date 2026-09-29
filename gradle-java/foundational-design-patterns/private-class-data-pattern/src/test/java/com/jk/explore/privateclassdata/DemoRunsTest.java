package com.jk.explore.privateclassdata;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", PrivateClassDataDemo.run());

    @Test
    void loose() {
        assertTrue(all.contains("first print:  INV-7: £90.00"));
        assertTrue(all.contains("second print: INV-7: £81.00"));
        assertTrue(all.contains("now says £81.00"));
    }

    @Test
    void protectedData() {
        assertTrue(all.contains("print 3: INV-7: £90.00"));
        assertTrue(all.contains("the invoice still says £100.00"));
        assertTrue(all.contains("InvoiceData setters: 0"));
        assertTrue(all.contains("times printed: 3; figures unchanged: £100.00"));
    }
}
