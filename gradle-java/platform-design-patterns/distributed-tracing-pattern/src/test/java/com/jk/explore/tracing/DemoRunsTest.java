package com.jk.explore.tracing;

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
            ProductPageDemo.main(new String[0]);
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
    @DisplayName("the numbers the narration quotes are the numbers the demo prints")
    void theQuotedNumbersAreReal() {
        String output = runTheDemo();

        // Act 1: the complaint.
        assertTrue(output.contains("It takes 900ms."), output);

        // Act 2: two customers, and two pricing calls nothing tells apart.
        assertTrue(output.contains("14:32:07.120  pricing          quote started"), output);
        assertTrue(output.contains("14:32:07.160  pricing          quote started"), output);

        // Act 3: the parent links that give the trace its shape.
        assertTrue(output.contains("ranking-model    span-6     parent span-5      340ms"), output);
        assertTrue(output.contains("product-page     span-1     parent (none)      900ms"), output);

        // Act 4: the answer, and the arithmetic behind it.
        assertTrue(output.contains("ranking-model     340ms   37% of the page"), output);
        assertTrue(output.contains("pricing           180ms   20% of the page"), output);
        assertTrue(output.contains("recommendations    60ms    6% of the page"), output);
        assertTrue(output.contains("slowest single piece of work is ranking-model, at 340ms"),
                output);
        assertTrue(output.contains("400ms, or 44% of what the customer waited for"), output);

        // Act 5: the wrong answer partial instrumentation produces.
        assertTrue(output.contains("appears to spend 60ms doing its own work"), output);

        // Act 6: the broken trace, and the same work drawn whole.
        assertTrue(output.contains("2 separate roots — this trace is broken"), output);
        assertTrue(output.contains("Two roots in one trace, and 400ms of work belonging to nobody"),
                output);
        assertTrue(output.contains("trace trace-async-fixed"), output);

        // Act 7: the sampling bill.
        assertTrue(output.contains("kept       10,000"), output);
        assertTrue(output.contains("discarded  990,000"), output);
        assertTrue(output.contains("request number 862,144"), output);
        assertTrue(output.contains("no — it is gone, and it is not recoverable"), output);
    }

    @Test
    @DisplayName("the culprit is named, and it is not the service anybody suspected")
    void theWaterfallNamesTheCulprit() {
        String output = runTheDemo();

        // The page span lasted the whole request and did none of the work. That
        // line is the reason total time never finds anybody.
        assertTrue(output.contains("900ms   0ms of it its own"), output);
    }

    @Test
    @DisplayName("the demo prints the same thing every run")
    void isDeterministic() {
        assertEquals(runTheDemo(), runTheDemo());
    }
}
