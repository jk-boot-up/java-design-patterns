package com.jk.explore.idempotentconsumerkafka;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/**
 * The demo is the document. Every number quoted in the README, in the slides and in the
 * narration is asserted here, so a change to the code that changes a figure fails the build
 * instead of quietly making the documents wrong.
 */
class DemoRunsTest {

    @Test
    void theSixActsRunAgainstARealBrokerAndDatabaseAndPrintTheFiguresTheDocumentsQuote() {
        assumeTrue(Broker.containerRuntimeAvailable(), "needs a container runtime");
        String out = runTheDemo();

        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        String[] figures = {
            "checkout places 3 orders, at places 0, 1, 2.",
            "is handed 3, queues 3 confirmation emails, and crashes before writing down its place. place written down: none.",
            "is handed the same orders again, at places 0, 1, 2. nothing on them says they are repeats.",
            "deliveries: 6 for 3 orders. confirmation emails queued: 6.",
            "it handles 3 orders, remembers 3 ids, and crashes",
            "copy B is handed the same 3. its list starts with 0 ids. confirmation emails queued: 6.",
            "so B skips 3 and queues 0.",
            "deliveries: 6. confirmation emails queued: 3. ids stored: 3.",
            "dies before writing the id. emails: 1, ids: 0.",
            "emails for ORD-1: 2.",
            "Postgres throws both away. emails: 0, ids: 0.",
            "handles it properly. emails: 1, ids: 1. exactly once",
            "after 3 seconds without asking for more, Kafka decides A is stuck",
            "sessions waiting on a lock: 1.",
            "queued by B: 0. emails for ORD-1: 1.",
            "Kafka refuses with CommitFailedException",
            "ids stored: 3. a cleanup job keeps ids for 24 hours, and deletes 3.",
            "this topic keeps orders for 168 hours. an operator replays the group from the start. handed again: 3. emails queued: 6.",
            "this demo needed 2 containers, a broker and a database, for 1 email per order.",
        };
        for (String figure : figures) {
            assertTrue(out.contains(figure), "missing: " + figure + "\n" + out);
        }
    }

    private static String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            KafkaIdempotentConsumerDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
