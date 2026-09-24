package com.jk.explore.claimchecks3;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import software.amazon.awssdk.services.s3.model.NoSuchKeyException;
import software.amazon.awssdk.services.sqs.model.SqsException;

/**
 * What S3 and SQS do, asked of them directly.
 *
 * <p>One LocalStack container is started for the whole class, because starting it is the slow
 * part, and removed at the end. Every wait is a bounded poll on something the services can be
 * asked; there is no sleep anywhere in this file.
 */
class RealS3AndSqsTest {

    private static LocalStack aws;

    @BeforeAll
    static void startLocalStack() {
        assumeTrue(LocalStack.containerRuntimeAvailable(), "needs a container runtime");
        aws = new LocalStack();
        aws.start();
    }

    @AfterAll
    static void stopLocalStack() {
        if (aws != null) {
            aws.close();
        }
    }

    @Test
    void sqsRefusesAMessageOneCharacterOverItsLimitAndTakesOneExactlyAtIt() {
        Queue queue = Queue.create(aws.sqs(), "limit-edge");
        int limit = queue.maximumMessageBytes();
        assertEquals(1_048_576, limit);
        queue.send("A".repeat(limit));
        SqsException refused = assertThrows(SqsException.class, () -> queue.send("A".repeat(limit + 1)));
        assertTrue(refused.awsErrorDetails().errorMessage().contains("Message must be shorter than 1048576 bytes"));
    }

    @Test
    void aPdfUnderTheLimitIsStillRefusedOnceItIsWrittenAsText() {
        Queue queue = Queue.create(aws.sqs(), "base64-grows");
        byte[] pdf = InvoicePdf.of("ORD-9001", 900_000);
        assertTrue(pdf.length < queue.maximumMessageBytes());
        assertThrows(SqsException.class, () -> new Sender(null, queue).sendWhole(pdf));
    }

    @Test
    void aTicketFetchesTheSameBytesAndClearsUpBoth() {
        Bucket bucket = Bucket.create(aws.s3(), "round-trip");
        Queue queue = Queue.create(aws.sqs(), "round-trip");
        byte[] pdf = InvoicePdf.of("ORD-9002", 1_500_000);
        Claim claim = new Sender(bucket, queue).send(pdf);
        assertEquals(36, claim.key().length());
        assertArrayEquals(pdf, new Receiver(bucket, queue).redeemNext());
        Poll.until("the ticket to be gone", () -> queue.waiting() == 0);
        assertEquals(0, bucket.keysListed());
    }

    @Test
    void overwritingAKeyIsCaughtByTheChecksumAndTheTicketStaysOnTheQueue() {
        Bucket bucket = Bucket.create(aws.s3(), "overwrite");
        Queue queue = Queue.create(aws.sqs(), "overwrite");
        Sender sender = new Sender(bucket, queue);
        sender.sendUnder("invoices/ORD-9003.pdf", InvoicePdf.of("ORD-9003", 10_000, 1));
        sender.sendUnder("invoices/ORD-9003.pdf", InvoicePdf.of("ORD-9003", 10_000, 2));
        assertEquals(1, bucket.versionsStored());
        assertThrows(Receiver.NotTheSamePayload.class, () -> new Receiver(bucket, queue).redeemNext());
        assertEquals(1, bucket.keysListed(), "nothing is deleted when the check fails");
    }

    @Test
    void inAVersionedBucketDeleteByKeyLeavesEveryVersionStored() {
        Bucket bucket = Bucket.create(aws.s3(), "versioned").keepEveryVersion();
        Queue queue = Queue.create(aws.sqs(), "versioned");
        Sender sender = new Sender(bucket, queue);
        byte[] first = InvoicePdf.of("ORD-9004", 10_000, 1);
        sender.sendUnder("invoices/ORD-9004.pdf", first);
        sender.sendUnder("invoices/ORD-9004.pdf", InvoicePdf.of("ORD-9004", 10_000, 2));
        assertArrayEquals(first, new Receiver(bucket, queue).redeemNext());
        assertEquals(0, bucket.keysListed());
        assertEquals(2, bucket.versionsStored());
        assertEquals(1, bucket.deleteMarkers());
        for (String version : bucket.versionIds("invoices/ORD-9004.pdf")) {
            bucket.delete("invoices/ORD-9004.pdf", version);
        }
        assertEquals(0, bucket.versionsStored());
    }

    @Test
    void aTicketWhoseLuggageIsGoneGetsNoSuchKeyAndStaysOnTheQueue() {
        Bucket bucket = Bucket.create(aws.s3(), "expiring").removeEverythingAfterDays(1);
        Queue queue = Queue.create(aws.sqs(), "expiring");
        Claim claim = new Sender(bucket, queue).send(InvoicePdf.of("ORD-9005", 10_000));
        assertTrue(ClaimCheckS3Demo.stampedForMidnightWithinTwoDays(bucket.expiryOf(claim.key())));
        assertEquals(345_600, queue.keepsUnreadSeconds());
        bucket.delete(claim.key());
        assertThrows(NoSuchKeyException.class, () -> new Receiver(bucket, queue).redeemNext());
    }

    @Test
    void aSendThatFailsAfterTheStoreLeavesAnObjectWithNoTicket() {
        Bucket bucket = Bucket.create(aws.s3(), "orphans");
        Queue queue = Queue.create(aws.sqs(), "orphans");
        Sender broken = new Sender(bucket, Queue.missing(aws.sqs(), queue));
        assertThrows(SqsException.class, () -> broken.send(InvoicePdf.of("ORD-9006", 10_000)));
        assertEquals(1, bucket.keysListed());
        assertEquals(0, queue.waiting());
    }
}
