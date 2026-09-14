package com.jk.explore.retry;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

/** The demo is teaching material, so a test keeps it working. */
class DemoRunsTest {

    @Test
    @DisplayName("the demo runs all four acts without throwing")
    void demoRuns() {
        assertDoesNotThrow(() -> RetryDemo.main(new String[0]));
    }
}
