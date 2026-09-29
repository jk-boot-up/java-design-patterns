package com.jk.explore.reactor;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", ReactorDemo.run());
    }

    @Test
    void threadPerConnection() {
        assertTrue(all.contains("100 shop tills connect and wait: 100 threads"));
    }

    @Test
    void reactor() {
        assertTrue(all.contains("threads running handlers: 1"));
        assertTrue(all.contains("100 tills ask at once: 100 correct answers"));
        assertTrue(all.contains("threads running handlers: still 1"));
    }

    @Test
    void slowHandler() {
        assertTrue(all.contains("it waited over 200 ms"));
    }
}
