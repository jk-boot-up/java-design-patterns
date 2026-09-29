package com.jk.explore.privateclassdata;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class InvoiceTest {

    @Test
    void printingDoesNotChangeTheFigures() {
        Invoice i = new Invoice("I", "c", 10000);
        assertEquals("I: £90.00", i.printWithStaffDiscount(10));
        assertEquals("I: £90.00", i.printWithStaffDiscount(10));
        assertEquals(10000, i.netPence());
        assertEquals(2, i.timesPrinted());
    }

    @Test
    void looseInvoiceDriftsWithEveryPrint() {
        LooseInvoice l = new LooseInvoice("I", 10000);
        l.printWithStaffDiscount(10);
        l.printWithStaffDiscount(10);
        assertEquals(8100, l.netPence());
    }

    @Test
    void dataHasNoSetters() {
        for (var m : InvoiceData.class.getDeclaredMethods()) {
            assertEquals(false, m.getName().startsWith("set"));
        }
    }
}
