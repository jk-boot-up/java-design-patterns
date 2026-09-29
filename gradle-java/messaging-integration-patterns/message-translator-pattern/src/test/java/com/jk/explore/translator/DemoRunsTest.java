package com.jk.explore.translator;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", MessageTranslatorDemo.run());

    @Test
    void oldWarehouse() {
        assertTrue(all.contains("sends XML: warehouse cannot read this order"));
    }

    @Test
    void translation() {
        assertTrue(all.contains("CSV        -> A-77 2 x MUG-1 £16.00"));
        assertTrue(all.contains("JSON       -> B-9 1 x TEAPOT-1 £25.00"));
        assertTrue(all.contains("marketplace C (XML): pick 1 x KETTLE-1 for C-5"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("\"Happy birthday, Mum\""));
    }
}
