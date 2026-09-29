package com.jk.explore.inputvalidation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class OrderParserTest {

    @Test
    void wordsForQuantityAreRefused() {
        OrderParser.Result r = OrderParser.parse(new OrderForm("MUG-1", "two", "a@b.co", "Ana"));
        assertEquals("quantity must be a whole number", r.problems().get(0));
    }

    @Test
    void quantityBoundaries() {
        assertEquals(1, new Quantity(1).value());
        assertEquals(99, new Quantity(99).value());
        assertThrows(IllegalArgumentException.class, () -> new Quantity(100));
    }

    @Test
    void hyphenatedNamesAreFair() {
        assertTrue(OrderParser.parse(new OrderForm("MUG-1", "1", "a@b.co", "Jean-Luc Ó Dálaigh")).ok());
    }

    @Test
    void markupInNameIsRefused() {
        assertTrue(!OrderParser.parse(new OrderForm("MUG-1", "1", "a@b.co", "<b>Ana</b>")).ok());
    }
}
