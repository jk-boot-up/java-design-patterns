package com.jk.explore.eventsourcing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The demo is what the video shows and what the documents quote, so its output is
 * pinned here. If a number in a narration line stops matching the program, this test
 * is what says so before a recording does.
 */
class DemoRunsTest {

    private String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            LoyaltyBalanceDemo.main(new String[0]);
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

        // Act 4: the balance the whole video is named after, and its four steps.
        assertTrue(output.contains("balance 60"), output);
        assertTrue(output.contains("balance 35"), output);
        assertTrue(output.contains("balance 155"), output);
        assertTrue(output.contains("balance 140"), output);

        // Act 3: the bug found months later, and the balance once it is ignored.
        assertTrue(output.contains("ORD-9001"), output);
        assertTrue(output.contains("2 times"), output);

        // Act 6: the cost of the fold and the cost with a snapshot.
        assertTrue(output.contains("5000"), output);
        assertTrue(output.contains("5001"), output);
        assertTrue(output.contains("502"), output);

        // Act 7: the snapshot that outlives the erasure.
        assertTrue(output.contains("30 points"), output);
    }

    @Test
    @DisplayName("the same run twice gives byte-identical output")
    void theDemoIsDeterministic() {
        // Fixed dates and no randomness anywhere, so the video can be re-recorded
        // months later and match the documents exactly.
        assertTrue(runTheDemo().equals(runTheDemo()));
    }
}
