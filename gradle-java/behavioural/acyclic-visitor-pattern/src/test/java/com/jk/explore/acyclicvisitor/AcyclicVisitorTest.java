package com.jk.explore.acyclicvisitor;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

class AcyclicVisitorTest {

    @Test
    void vatOnlyOnElectronics() {
        Visitors.Vat vat = new Visitors.Vat();
        AcyclicVisitorDemo.BASKET.forEach(p -> p.accept(vat));
        assertEquals(600, vat.vatPence());
    }

    @Test
    void classicAndAcyclicAgree() {
        Visitors.Vat vat = new Visitors.Vat();
        Visitors.ClassicVat classic = new Visitors.ClassicVat();
        AcyclicVisitorDemo.BASKET.forEach(p -> {
            p.accept(vat);
            p.acceptClassic(classic);
        });
        assertEquals(classic.vatPence(), vat.vatPence());
    }

    @Test
    void unsupportedTypeIsSkippedNotBroken() {
        assertFalse(new Products.GiftCard("G", 1).accept(new Visitors.Vat()));
    }

    @Test
    void classicCannotTakeANewType() {
        assertThrows(UnsupportedOperationException.class,
                () -> new Products.GiftCard("G", 1).acceptClassic(new Visitors.ClassicVat()));
    }

    @Test
    void customsHandlesOnlyElectronics() {
        Visitors.Customs c = new Visitors.Customs();
        assertTrue(new Products.Electronics("K", 1, 1200).accept(c));
        assertFalse(new Products.Book("B", 1).accept(c));
        assertEquals(List.of("form for K, 1200 g"), c.forms());
    }

    @Test
    void rootInterfaceNamesNoProduct() {
        assertEquals(0, ProductVisitor.class.getDeclaredMethods().length);
    }
}
