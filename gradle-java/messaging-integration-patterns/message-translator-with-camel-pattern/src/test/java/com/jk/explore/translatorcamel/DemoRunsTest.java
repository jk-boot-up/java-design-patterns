package com.jk.explore.translatorcamel;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", CamelTranslatorDemo.run());
        assertTrue(all.contains("Camel refuses: no type converter from String to OrderMessage"));
        assertTrue(all.contains("CSV (unmarshal().csv())               -> pick 2 x MUG-1 for A-77"));
        assertTrue(all.contains("JSON (unmarshal().json(Jackson))      -> pick 1 x TEAPOT-1 for B-9"));
        assertTrue(all.contains("routes running: 5"));
        assertTrue(all.contains("before: no consumers available on endpoint direct://translate-xml"));
        assertTrue(all.contains("translate-xml: pick 1 x KETTLE-1 for C-5"));
        assertTrue(all.contains("more than 20 library files"));
    }
}
