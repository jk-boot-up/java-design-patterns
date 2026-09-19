package com.jk.explore.threadpool;

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
            PackingTeamDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }

    @Test
    void allSixActsRunAndProduceRealNumbers() throws InterruptedException {
        String output = runTheDemo();

        assertTrue(output.contains("ONE. A thread per order"), output);
        assertTrue(output.contains("TWO. A fixed pool with the queue nobody chose"), output);
        assertTrue(output.contains("THREE. The pattern"), output);
        assertTrue(output.contains("FOUR. Sizing the pool"), output);
        assertTrue(output.contains("FIVE. Pool starvation"), output);
        assertTrue(output.contains("SIX. Java's answer"), output);

        assertTrue(output.contains("created 2,000 real threads"), output);
        assertTrue(output.contains("backlog waiting behind the 2 busy workers: 500"), output);
        assertTrue(output.contains("queue filled to capacity 3: 3"), output);
        assertTrue(output.contains("REJECTED on the spot"), output);
        assertTrue(output.contains("starved: true"), output);
        assertTrue(output.contains("created 2,000 virtual threads"), output);
    }
}
