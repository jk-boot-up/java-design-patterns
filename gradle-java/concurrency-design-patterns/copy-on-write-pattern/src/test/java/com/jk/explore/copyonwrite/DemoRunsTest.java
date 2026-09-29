package com.jk.explore.copyonwrite;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", CopyOnWriteDemo.run());
    }

    @Test
    void plainListFails() {
        assertTrue(all.contains("ConcurrentModificationException after: [web page cache, loyalty service]"));
    }

    @Test
    void cowWorks() {
        assertTrue(all.contains("first change reached: [web page cache, loyalty service, phone app]"));
        assertTrue(all.contains("next change reached:  [web page cache, loyalty service, phone app, email service]"));
        assertTrue(all.contains("failures: 0"));
        assertTrue(all.contains("started with 3 listeners; the list now has 4"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("49,995,000 references copied"));
    }
}
