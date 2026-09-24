package com.jk.explore.claimchecks3;

import java.util.Base64;
import java.util.UUID;

/**
 * Checkout's side. It has an invoice to hand to the email service, and two ways to do it.
 */
public class Sender {

    private final Bucket bucket;
    private final Queue queue;

    public Sender(Bucket bucket, Queue queue) {
        this.bucket = bucket;
        this.queue = queue;
    }

    /**
     * Without the pattern: the whole PDF goes in the message. A message is text, so the bytes
     * are written out as base64, which spells every 3 bytes with 4 letters.
     */
    public static String asMessageText(byte[] pdf) {
        return Base64.getEncoder().encodeToString(pdf);
    }

    public void sendWhole(byte[] pdf) {
        queue.send(asMessageText(pdf));
    }

    /**
     * The claim check: store the PDF under a random key nobody could guess, then send only the
     * ticket. Storing comes first, so the luggage is there before anybody holds its ticket.
     */
    public Claim send(byte[] pdf) {
        return sendUnder(UUID.randomUUID().toString(), pdf);
    }

    /** The same, but with a key the caller chooses, such as one made from the order id. */
    public Claim sendUnder(String key, byte[] pdf) {
        Bucket.Stored stored = bucket.put(key, pdf);
        Claim claim = new Claim(bucket.name(), key, stored.versionId(), pdf.length, Claim.checksum(pdf));
        queue.send(claim.toText());
        return claim;
    }
}
