package com.jk.explore.bulkhead;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

/** The demo is teaching material, so a test keeps it working. */
class DemoRunsTest {

    @Test
    @DisplayName("the demo runs all four acts and shuts every pool down")
    void demoRuns() {
        assertDoesNotThrow(() -> BulkheadDemo.main(new String[0]));
    }
}
