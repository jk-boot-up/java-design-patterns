package com.jk.explore.pubsubredis;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/**
 * The demo is the document. Every figure quoted in the README, the slides and the narration
 * is asserted here, so a change that moves a number fails the build instead of quietly
 * making the documents wrong.
 */
class DemoRunsTest {

    @Test
    void theSixActsRunAgainstARealRedisAndPrintTheFiguresTheDocumentsQuote() {
        assumeTrue(RedisServer.containerRuntimeAvailable(), "needs a container runtime");
        String out = runTheDemo();

        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("inventory [ORD-1], email [ORD-1], analytics [ORD-1]."), out);
        assertTrue(out.contains("knows 3 services by name."), out);
        assertTrue(out.contains("published OrderPlaced ORD-1 once. Redis answered: 3 receivers."), out);
        assertTrue(out.contains("ORD-2 is published: 4 receivers."), out);
        assertTrue(out.contains("the loyalty process printed [ORD-2] and exited with code 0."), out);
        assertTrue(out.contains("3 orders published while only email listened. Redis answered: [1, 1, 1]."), out);
        assertTrue(out.contains("ORD-4 is published: 2 receivers."), out);
        assertTrue(out.contains("email saw [ORD-1, ORD-2, ORD-3, ORD-4]. loyalty saw [ORD-4]."), out);
        assertTrue(out.contains("keys in the database: 0."), out);
        assertTrue(out.contains("OrderPlaced ORD-1 reached 2 receivers. OrderCancelled ORD-1 reached 1."), out);
        assertTrue(out.contains("analytics listened to orders.*: [OrderPlaced ORD-1, OrderCancelled ORD-1]."), out);
        assertTrue(out.contains("out of the box: 32mb, or 8mb for 60 seconds."), out);
        assertTrue(out.contains("this demo lowers it to 1mb."), out);
        assertTrue(out.contains("in rounds of 1000"), out);
        assertTrue(out.contains("more than 10,000 orders later, Redis cut analytics off. listeners cut off for falling behind: 1."), out);
        assertTrue(out.contains("the first order reached 2 receivers, the last reached 1. email kept up and received every one."), out);
        assertTrue(out.contains("got some of them, not all, then its connection ended."), out);
        assertTrue(out.contains("Redis told the order service: 0 receivers."), out);
        assertTrue(out.contains("email came back and got: []."), out);
        assertTrue(out.contains("1 container and 2 Java processes."), out);
    }

    private static String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            RedisPubSubDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
