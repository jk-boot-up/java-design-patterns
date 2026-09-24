package com.jk.explore.loadlevelingsqs;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/**
 * The demo is the document. Every number quoted in the README, in the slides and in the
 * narration is asserted here, so a change that moves a figure fails the build instead of
 * quietly making the documents wrong.
 */
class DemoRunsTest {

    @Test
    void theSixActsRunAgainstLocalStackAndPrintTheFiguresTheDocumentsQuote() {
        assumeTrue(LocalStack.containerRuntimeAvailable(), "needs a container runtime");
        String out = runTheDemo();

        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        String[] figures = {
            "11 orders in one request: Maximum number of entries per request are 10. You have sent 11.",
            "so the burst goes as 10 requests of 10. SQS reports 100 waiting and 0 in flight.",
            "for 345600 seconds, which is 4 days.",
            "asks for 11 at once: Value 11 for parameter MaxNumberOfMessages is invalid. Reason: Must be between 1 and 10, if provided.",
            "it takes 10. SQS now reports 90 waiting and 10 in flight",
            "waiting after each round: 90, 80, 70, 60, 50, 40, 30, 20, 10, 0.",
            "100 packed in 10 rounds, never more than 10 at once. the deepest the queue got: 100.",
            "the default is 30 seconds.",
            "this queue's timeout is 2 seconds. a packer takes ORD-2001 and stops before it finishes. SQS reports 0 waiting and 1 in flight.",
            "a second packer asks at once, and is given 0 orders.",
            "ORD-2001 comes back once the 2 seconds have passed, not before: true. SQS has now handed it out 2 times.",
            "packer B is given ORD-3001 too.",
            "ORD-3001 was packed 2 times",
            "hide it 10 seconds more.",
            "hold its question open for 3 seconds, past the old timeout. it is given 0 orders.",
            "ORD-3002 was packed 1 time.",
            "the packer takes 10, finishes 3, and its process stops.",
            "SQS reports 90 waiting and 7 in flight. nothing is lost; 7 are only hidden.",
            "they come back: 97 waiting.",
            "packed: 100, lost: 0, packed twice: 0. orders SQS handed out a second time: 7.",
            "SQS answers: Unknown Attribute MaximumDepth.",
            "for 20 rounds. SQS refused none. waiting: 100, and growing.",
            "30 requests (SendMessageBatch x10, ReceiveMessage x10, DeleteMessageBatch x10). one at a time: 300.",
            "1 container for 1 queue service.",
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
            LoadLevelingSqsDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
