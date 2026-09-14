package com.jk.explore.idempotentconsumer;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** Keeps the demo honest: if it stops running, the build says so. */
class DemoRunsTest {

    @Test
    @DisplayName("the demo runs all five acts without blowing up")
    void theDemoRuns() {
        assertDoesNotThrow(() -> OrderPlacedTwiceDemo.main(new String[0]));
    }
}
