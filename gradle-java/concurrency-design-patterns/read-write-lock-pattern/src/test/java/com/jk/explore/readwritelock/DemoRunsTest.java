package com.jk.explore.readwritelock;

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
            CatalogueDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }

    @Test
    void allSixActsRunAndProduceRealNumbers() throws InterruptedException {
        String output = runTheDemo();

        assertTrue(output.contains("ONE. No lock at all"), output);
        assertTrue(output.contains("TWO. One mutual-exclusion lock"), output);
        assertTrue(output.contains("THREE. The pattern"), output);
        assertTrue(output.contains("FOUR. The mechanism behind writer starvation"), output);
        assertTrue(output.contains("FIVE. Upgrading a read lock"), output);
        assertTrue(output.contains("SIX. When the lock loses"), output);

        assertTrue(output.contains("read mid-update: 54.99 GBP"), output);
        assertTrue(output.contains("writer genuinely queued, waiting: true"), output);
        assertTrue(output.contains("a second reader's tryLock() barged past it anyway: true"), output);
        assertTrue(output.contains("deadlocked: true"), output);
    }
}
