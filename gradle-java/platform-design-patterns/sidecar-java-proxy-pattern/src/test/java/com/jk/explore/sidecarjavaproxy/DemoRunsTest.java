package com.jk.explore.sidecarjavaproxy;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The demo is what the video shows and what the written documents quote, so its output
 * is pinned here. If a number in a narration line stops matching the program, this test
 * is what says so before a recording does.
 */
class DemoRunsTest {

    private String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            ProxySwapDemo.main(new String[0]);
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
    @DisplayName("nginx's three attempts arrive at 1, 2 and 3 milliseconds")
    void quotesTheNginxArrivalTimes() {
        String output = runTheDemo();

        assertTrue(output.contains("attempt at    1ms   declined"));
        assertTrue(output.contains("attempt at    2ms   declined"));
        assertTrue(output.contains("attempt at    3ms   declined"));
        assertTrue(output.contains("3 attempts, first to last: 2ms"));
    }

    @Test
    @DisplayName("the java proxy's three attempts arrive at 1, 202 and 603 milliseconds")
    void quotesTheJavaProxyArrivalTimes() {
        String output = runTheDemo();

        assertTrue(output.contains("attempt at  202ms   declined"));
        assertTrue(output.contains("attempt at  603ms   charged"));
        assertTrue(output.contains("3 attempts, first to last: 602ms"));
    }

    @Test
    @DisplayName("the service is on start number 1 on both sides of the swap")
    void showsTheServiceNeverRestarting() {
        String output = runTheDemo();

        assertEquals(2, count(output, "checkout is on start number:       1"));
        assertTrue(output.contains("payments services ever started:    1"));
        assertTrue(output.contains("times the service has restarted:   0"));
        assertTrue(output.contains("times the port has been replaced:  2"));
    }

    @Test
    @DisplayName("the same payment fails through one proxy and succeeds through the other")
    void showsBothOutcomesForTheSamePayment() {
        String output = runTheDemo();

        assertTrue(output.contains("ORD-4418     £47.99    NOT PAID"));
        assertTrue(output.contains("ORD-4418     £47.99    pay_ORD-4418 (3 attempts, 603ms waiting)"));
    }

    @Test
    @DisplayName("the mid-swap window reaches the provider zero times")
    void showsTheEmptyPort() {
        String output = runTheDemo();

        assertTrue(output.contains("connection refused to localhost:8081"));
        assertTrue(output.contains("attempts that reached the provider: 0"));
    }

    @Test
    @DisplayName("the closing table names both languages and both line counts")
    void printsTheComparison() {
        String output = runTheDemo();

        assertTrue(output.contains("nginx        nginx configuration      22"));
        assertTrue(output.contains("java-proxy   Java                     40"));
        assertTrue(output.contains("what nginx has no words for:"));
        assertTrue(output.contains("wait 200ms between attempts, doubling"));
        assertTrue(output.contains("what java-proxy has no words for:\n    nothing"));
    }

    @Test
    @DisplayName("every line fits in the 76 columns a slide has room for")
    void everyLineFitsOnASlide() {
        for (String line : runTheDemo().split("\n")) {
            assertTrue(line.length() <= 76,
                    "line is " + line.length() + " columns: " + line);
        }
    }

    private int count(String haystack, String needle) {
        int found = 0;
        for (int at = haystack.indexOf(needle); at >= 0;
                at = haystack.indexOf(needle, at + needle.length())) {
            found++;
        }
        return found;
    }
}
