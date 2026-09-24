package com.jk.explore.claimchecks3;

import java.util.Arrays;

/**
 * The email service's side. It takes a ticket off the queue, fetches the luggage, checks it,
 * and only then clears up both.
 */
public class Receiver {

    /** The luggage fetched with a ticket is not the luggage the ticket was written for. */
    public static class NotTheSamePayload extends RuntimeException {
        public NotTheSamePayload(String message) {
            super(message);
        }
    }

    private final Bucket bucket;
    private final Queue queue;

    public Receiver(Bucket bucket, Queue queue) {
        this.bucket = bucket;
        this.queue = queue;
    }

    /**
     * Takes one ticket and redeems it. The object is deleted by key once the bytes check out,
     * then the message is deleted, so a crash in between leaves the ticket to be tried again.
     * If the check fails, nothing is deleted.
     */
    public byte[] redeemNext() {
        Queue.Received received = queue.take();
        Claim claim = Claim.read(received.body());
        byte[] pdf = claim.versionId() == null ? bucket.get(claim.key()) : bucket.get(claim.key(), claim.versionId());
        if (pdf.length != claim.size() || !Claim.checksum(pdf).equals(claim.sha256())) {
            throw new NotTheSamePayload("the payload is not the one that was sent: the checksum does not match");
        }
        bucket.delete(claim.key());
        queue.delete(received);
        return pdf;
    }

    public static boolean same(byte[] a, byte[] b) {
        return Arrays.equals(a, b);
    }
}
