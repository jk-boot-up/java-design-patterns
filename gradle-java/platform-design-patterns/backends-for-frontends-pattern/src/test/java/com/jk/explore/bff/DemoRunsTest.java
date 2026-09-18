package com.jk.explore.bff;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

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
            ProductScreenDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }

    @Test
    @DisplayName("the demo runs end to end and prints all seven acts")
    void allSevenActsRun() {
        String output = runTheDemo();

        for (int act = 1; act <= 7; act++) {
            assertTrue(output.contains("Act " + act + " —"), "missing act " + act);
        }
    }

    @Test
    @DisplayName("the quoted round-trip counts are the ones the program measured")
    void quotesTheRoundTripsItMeasured() {
        String output = runTheDemo();

        assertTrue(output.contains("calls from the phone:   5"),
                "Act 1 should measure five calls from the device");
        assertTrue(output.contains("calls from the phone:   1"),
                "Act 2 should measure one call from the device");
    }

    @Test
    @DisplayName("the drift in Act 5 is visible in the output, not merely described")
    void showsTheTwoScreensDisagreeing() {
        String output = runTheDemo();

        assertTrue(output.contains("(nothing — no saving may be claimed for this price)"),
                "the desktop store should claim nothing");
        assertTrue(output.contains("phone app says:      Save £12.00"),
                "the phone should claim a saving the shop may not advertise");
    }

    @Test
    @DisplayName("the comparison table prints all three designs")
    void printsTheComparison() {
        String output = runTheDemo();

        assertTrue(output.contains("five calls from the phone"));
        assertTrue(output.contains("one shared endpoint"));
        assertTrue(output.contains("a backend for the phone"));
    }
}
