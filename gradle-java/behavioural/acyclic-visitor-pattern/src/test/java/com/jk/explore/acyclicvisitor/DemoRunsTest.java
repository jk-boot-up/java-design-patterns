package com.jk.explore.acyclicvisitor;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", AcyclicVisitorDemo.run());

    @Test
    void classic() {
        assertTrue(all.contains("VAT on a book, tea and a kettle: £6.00"));
        assertTrue(all.contains("ClassicVisitor has 3 methods"));
        assertTrue(all.contains("a gift card arrives: ClassicVisitor has no visitGiftCard"));
    }

    @Test
    void acyclic() {
        assertTrue(all.contains("Book, Food and Electronics visitors: £6.00"));
    }

    @Test
    void newType() {
        assertTrue(all.contains("VAT visitor skips GIFT-1"));
        assertTrue(all.contains("handled: [GIFT-1]"));
    }

    @Test
    void customs() {
        assertTrue(all.contains("handled 1 of 4"));
        assertTrue(all.contains("[form for KETTLE-1, 1200 g]"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("tea accepted: false, and nobody was told"));
    }
}
