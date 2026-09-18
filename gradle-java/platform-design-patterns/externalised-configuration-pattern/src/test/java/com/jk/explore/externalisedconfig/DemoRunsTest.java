package com.jk.explore.externalisedconfig;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The demo is what the video shows and what the documents quote, so its output is
 * pinned here. If a number in a narration line stops matching the program, this
 * test is what says so before a recording does.
 */
class DemoRunsTest {

    private String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            FreeDeliveryDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }

    @Test
    @DisplayName("the demo runs end to end and prints all nine acts")
    void allNineActsRun() {
        String output = runTheDemo();

        for (int act = 1; act <= 9; act++) {
            assertTrue(output.contains("Act " + act + " -"), "missing act " + act);
        }
    }

    @Test
    @DisplayName("the numbers the narration quotes are the numbers the demo prints")
    void theQuotedNumbersAreReal() {
        String output = runTheDemo();

        // Act 1 and 3: the two thresholds and the basket that moves between them.
        assertTrue(output.contains("free delivery over £50.00"), output);
        assertTrue(output.contains("ORD-7102  goods £48.00  delivery FREE"), output);

        // Act 2: the cost of the naive version, and the weekend it misses.
        assertTrue(output.contains("total work: 2 hours 15 minutes"), output);
        assertTrue(output.contains("live at:    Mon 10 Mar 10:45"), output);
        assertTrue(output.contains("late by 2 days 1 hour 45 minutes"), output);

        // Act 5: every basket free, including the smallest one.
        assertTrue(output.contains("ORD-7103  goods £31.50  delivery FREE"), output);
        assertTrue(output.contains("reached the running shop in 4 seconds"), output);

        // Act 7: the declared schema, and the last good value surviving.
        assertTrue(output.contains("delivery.freeOver: money, £5.00 to £200.00,"
                + " default £50.00"), output);
        assertTrue(output.contains("last value that passed validation"), output);

        // Act 8 and 9: the audit trail, and the rollback four seconds later.
        assertTrue(output.contains("5 changes to one setting in under a day"), output);
        assertTrue(output.contains("Sat 08 Mar 11:40:08"), output);
        assertTrue(output.contains("live Mon 10 Mar 11:15"), output);
    }

    @Test
    @DisplayName("the audit trail printed in act 8 has all five changes in order")
    void theAuditTrailIsComplete() {
        String output = runTheDemo();

        assertTrue(output.contains("#1  Fri 07 Mar 16:30:04"), output);
        assertTrue(output.contains("#2  Sat 08 Mar 09:12:04"), output);
        assertTrue(output.contains("#3  Sat 08 Mar 09:20:04"), output);
        assertTrue(output.contains("#4  Sat 08 Mar 10:05:04"), output);
        assertTrue(output.contains("#5  Sat 08 Mar 11:40:04"), output);
        assertTrue(output.contains("by on-call (rollback)"), output);
    }

    @Test
    @DisplayName("the same run twice gives identical output")
    void theDemoIsDeterministic() {
        // Fixed dates and no randomness anywhere, so the video can be re-recorded
        // months later and match the documents exactly.
        assertEquals(runTheDemo(), runTheDemo());
    }
}
