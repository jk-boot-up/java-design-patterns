package com.jk.explore.blackboard;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", BlackboardDemo.run());

    @Test
    void everyCheckInOrder() {
        assertTrue(all.contains("REJECT after all 6 checks, 902 ms"));
    }

    @Test
    void goodOrderApproved() {
        assertTrue(all.contains("good order: APPROVE, risk 0, 6 checks, 902 ms"));
    }

    @Test
    void stopsEarly() {
        assertTrue(all.contains("REJECT at risk 70 after 5 checks, 102 ms"));
    }

    @Test
    void newCheck() {
        assertTrue(all.contains("£300: REJECT, +60 risk, over £200 of gift cards"));
        assertTrue(all.contains("would have been: APPROVE"));
    }
}
