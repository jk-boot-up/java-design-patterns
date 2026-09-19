package com.jk.explore.futurepromise;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertTrue;

class DemoRunsTest {

    private String runTheDemo() throws Exception {
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
    void allSixActsRunAndProduceRealNumbers() throws Exception {
        String output = runTheDemo();

        assertTrue(output.contains("ONE. Sequential"), output);
        assertTrue(output.contains("TWO. Concurrent"), output);
        assertTrue(output.contains("THREE. Future and Promise"), output);
        assertTrue(output.contains("FOUR. Exceptions move"), output);
        assertTrue(output.contains("FIVE. get() with no timeout"), output);
        assertTrue(output.contains("SIX. Cancellation is cooperative"), output);

        assertTrue(output.contains("price £129.99, stock 7, rating 4.6"));
        assertTrue(output.contains("cause: catalogue unavailable for ESP-001"));
        assertTrue(output.contains("timed out: true"));
        assertTrue(output.contains("cancel(true) reported: true"));
        assertTrue(output.contains("the task ran to completion anyway: true"));
    }
}
