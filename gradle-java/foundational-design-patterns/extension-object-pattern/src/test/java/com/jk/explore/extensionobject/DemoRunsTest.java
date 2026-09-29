package com.jk.explore.extensionobject;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", ExtensionObjectDemo.run());

    @Test
    void fat() {
        assertTrue(all.contains("FatProduct has 8 fields; a mug leaves 5 of them empty"));
    }

    @Test
    void roles() {
        assertTrue(all.contains("e-book roles: [Download]; kettle: [Warranty]; mug: []"));
        assertTrue(all.contains("EBOOK-1: email link https://shop.example/d/EBOOK-1 (3 downloads)"));
        assertTrue(all.contains("KETTLE-1: register a 2-year warranty"));
    }

    @Test
    void newRole() {
        assertTrue(all.contains("BEANS-1: schedule a delivery every 4 weeks"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("without its Download role: 0 actions"));
    }
}
