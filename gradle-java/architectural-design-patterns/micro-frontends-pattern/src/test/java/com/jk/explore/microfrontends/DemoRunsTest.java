package com.jk.explore.microfrontends;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", MicroFrontendsDemo.run());
    }

    @Test
    void oneFrontEnd() {
        assertTrue(all.contains("the whole page fails"));
    }

    @Test
    void fragments() {
        assertTrue(all.contains("[recommendations] (recommendations unavailable)"));
        assertTrue(all.contains("free delivery over £40 | [recommendations] mug, teapot"));
        assertTrue(all.contains("1 page + 3 fragment requests"));
        assertTrue(all.contains("[product] steel kettle, 30.00 GBP"));
    }
}
