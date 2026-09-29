package com.jk.explore.markerinterface;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", MarkerInterfaceDemo.run());

    @Test
    void tags() {
        assertTrue(all.contains("MILK-1: ice packs"));
        assertTrue(all.contains("MILK-2: plain box"));
        assertTrue(all.contains("CREAM-1: plain box"));
    }

    @Test
    void markers() {
        assertTrue(all.contains("MUG-1: bubble wrap"));
        assertTrue(all.contains("KETTLE-1: plain box"));
        assertTrue(all.contains("Perishable has 0 methods"));
        assertTrue(all.contains("chilled van takes MILK-1"));
        assertTrue(all.contains("YOG-6: ice packs"));
    }
}
