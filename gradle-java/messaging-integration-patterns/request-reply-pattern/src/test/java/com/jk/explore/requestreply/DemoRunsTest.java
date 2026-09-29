package com.jk.explore.requestreply;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", RequestReplyDemo.run());
    }

    @Test
    void inOrder() {
        assertTrue(all.contains("reserve KETTLE-1 x 5 -> RESERVED 2 x MUG-1"));
    }

    @Test
    void correlated() {
        assertTrue(all.contains("WEB-1 reserve KETTLE-1 x 5 -> REFUSED 5 x KETTLE-1"));
        assertTrue(all.contains("WEB-2 reserve MUG-1 x 2 -> RESERVED 2 x MUG-1"));
        assertTrue(all.contains("phone app APP-1 -> RESERVED 1 x TEAPOT-1"));
        assertTrue(all.contains("20 answered and matched"));
    }

    @Test
    void lost() {
        assertTrue(all.contains("WEB-24: no reply after 500 ms"));
        assertTrue(all.contains("still in the waiting table: 1"));
    }
}
