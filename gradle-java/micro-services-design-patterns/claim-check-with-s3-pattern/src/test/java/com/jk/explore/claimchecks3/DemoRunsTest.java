package com.jk.explore.claimchecks3;

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
            "it reports its longest message as 1048576 bytes.",
            "a PDF of 1500000 bytes. a message is text, so it goes as base64: 2000000 characters.",
            "SQS refuses it: Message must be shorter than 1048576 bytes.",
            "a PDF of 786432 bytes becomes 1048576 characters and is accepted. one byte more, 786433, becomes 1048580 and is refused.",
            "under a random key of 36 characters",
            "the ticket is 113 bytes of text: bucket, key, size 1500000, checksum bb8711d26a6daf29.",
            "fetches 1500000 bytes, identical to what was sent: true.",
            "objects left in the bucket: 0. messages waiting: 0.",
            "S3 still holds 4 invoices, and SQS still holds 4 tickets for them.",
            "its send fails: The specified queue does not exist.",
            "S3 now holds 5 invoices and SQS holds 4 tickets. 1 invoice has no ticket",
            "S3 keeps 1 object.",
            "the email service redeems the first ticket: the payload is not the one that was sent: the checksum does not match.",
            "first ticket, identical to the first invoice: true.",
            "keys listed: 0. versions still stored: 2. delete markers: 1.",
            "deleting each version by its id: 0 stored.",
            "between 24 and 48 hours away: true.",
            "for 345600 seconds, which is 4 days.",
            "tickets still waiting: 1.",
            "a slow email service redeems it: The specified key does not exist.",
            "a 600000-byte invoice sent whole: 3 requests (SendMessage, ReceiveMessage, DeleteMessage). the queue carried 800000 bytes.",
            "by ticket: 6 requests (PutObject, SendMessage, ReceiveMessage, GetObject, DeleteObject, DeleteMessage). the queue carried 117 bytes.",
            "1 container for 1 queue service and 1 storage service.",
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
            ClaimCheckS3Demo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
