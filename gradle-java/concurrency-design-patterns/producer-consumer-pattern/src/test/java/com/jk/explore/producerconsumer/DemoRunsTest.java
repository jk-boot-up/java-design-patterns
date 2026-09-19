package com.jk.explore.producerconsumer;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertTrue;

class DemoRunsTest {

    private String runTheDemo() throws InterruptedException {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            PackingWarehouseDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }

    @Test
    void allFiveActsRunAndProduceRealNumbers() throws InterruptedException {
        String output = runTheDemo();

        assertTrue(output.contains("ONE. No queue at all"), output);
        assertTrue(output.contains("TWO. A thread per order"), output);
        assertTrue(output.contains("THREE. The bounded queue"), output);
        assertTrue(output.contains("FOUR. Clean shutdown"), output);
        assertTrue(output.contains("FIVE. Abrupt shutdown"), output);
        assertTrue(output.contains("created 2,000 real threads"), output);
        assertTrue(output.contains("queue filled to capacity 3: 3"), output);
        assertTrue(output.contains(
                "one more order, offered with a 150ms patience: REJECTED"), output);
        assertTrue(output.contains("packed before stopping: 4 of 4"), output);
        assertTrue(output.contains("orders lost, still in the queue: 4"), output);
    }
}
