package com.jk.explore.sidecar;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The demo is what the video shows and what the written notes quote, so its output is
 * pinned here. If a number in a narration line stops matching the program, this test is
 * what says so before a recording does.
 */
class DemoRunsTest {

    private String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            PaymentsDemo.main(new String[0]);
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
    @DisplayName("the sixteen copies and four edit sites are the ones it computed")
    void quotesTheCopyCounts() {
        String output = runTheDemo();

        assertTrue(output.contains("copies of a cross-cutting decision: 16"));
        assertTrue(output.contains("places to edit to change one:       4"));
    }

    @Test
    @DisplayName("the grid shows three services updated and the fourth left behind")
    void showsThreeUpdatedAndOneMissed() {
        String output = runTheDemo();

        assertTrue(output.contains("checkout                     3    200ms"));
        assertTrue(output.contains("refunds                      3    200ms"));
        assertTrue(output.contains("marketplace-payouts          3    200ms"));
        assertTrue(output.contains("subscription-billing         6     10ms"));
    }

    @Test
    @DisplayName("the incident prints the payouts failure and the thirteenth attempt")
    void quotesTheIncident() {
        String output = runTheDemo();

        assertTrue(output.contains("NOT PAID"));
        assertTrue(output.contains("429 refused"));
        assertTrue(output.contains("total                 13 of 12 allowed, 1 refused"));
    }

    @Test
    @DisplayName("with sidecars the same night spends twelve attempts and refuses none")
    void quotesTheRepairedNight() {
        String output = runTheDemo();

        assertTrue(output.contains("total                 12 of 12 allowed, 0 refused"));
        assertTrue(output.contains("Four payments, twelve attempts, nobody refused."));
    }

    @Test
    @DisplayName("the comparison table prints all three rows, including the worse one")
    void printsTheHonestTable() {
        String output = runTheDemo();

        assertTrue(output.contains("copies of a cross-cutting decision            16         4"));
        assertTrue(output.contains("places to edit for one policy change           4         1"));
        assertTrue(output.contains("processes to run and patch                     4         8"));
    }

    @Test
    @DisplayName("stopping the sidecar sends nothing at all to the gateway")
    void quotesTheZeroAttempts() {
        String output = runTheDemo();

        assertTrue(output.contains("connection refused to localhost"));
        assertTrue(output.contains("attempts that reached the gateway: 0"));
    }

    @Test
    @DisplayName("the hop is quoted as three milliseconds over three attempts")
    void quotesTheHop() {
        String output = runTheDemo();

        assertTrue(output.contains("retry code inside the service      3 attempts, 600ms"));
        assertTrue(output.contains("retry code in a proxy next door    3 attempts, 603ms"));
        assertTrue(output.contains("3 milliseconds, which is 1ms per attempt"));
    }

    @Test
    @DisplayName("the demo admits in words that this is Decorator in one program")
    void admitsItIsDecoratorInOneJvm() {
        String output = runTheDemo();

        assertTrue(output.contains("Decorator pattern"));
        assertTrue(output.contains("It is"));
        assertTrue(output.contains("where the code runs"));
    }

    @Test
    @DisplayName("every printed line fits the width a slide can show")
    void everyLineFitsOnASlide() {
        for (String line : runTheDemo().split("\n")) {
            assertTrue(line.length() <= 76,
                    "too wide for a slide (" + line.length() + "): " + line);
        }
    }

    @Test
    @DisplayName("nothing is priced in anything but pounds")
    void everyAmountIsInPounds() {
        String output = runTheDemo();

        assertTrue(output.contains("£47.99"));
        assertTrue(output.contains("£186.40"));
        assertFalse(output.contains("$"));
    }
}
