package com.jk.explore.claimcheck;

import java.util.Arrays;

public class ClaimCheckDemo {

    static final int LIMIT = 1000;

    static byte[] invoicePdf(int bytes) {
        byte[] b = new byte[bytes];
        for (int i = 0; i < bytes; i++) {
            b[i] = (byte) ('A' + i % 26);
        }
        return b;
    }

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. A message that is too big.");
        Broker broker = new Broker(LIMIT);
        try {
            broker.publish(new Broker.Message("invoice", invoicePdf(5000)));
        } catch (MessageTooLarge e) {
            System.out.println("  the invoice is 5000 bytes. " + e.getMessage() + ".");
        }
        System.out.println("  most brokers cap the size of a message, and the ones that do not get slow when messages are large.");
    }

    private static void two() {
        System.out.println("TWO. Send the ticket, not the luggage.");
        Broker broker = new Broker(LIMIT);
        BlobStore store = new BlobStore(new Clock(), 60);
        Claim claim = new Sender(broker, store).send("invoice", invoicePdf(5000));
        System.out.println("  the invoice is stored. the message carries a claim: an id of " + claim.blobId().length() + " characters, size " + claim.size() + ", checksum " + claim.sha256() + ".");
        byte[] got = new Receiver(broker, store).receive();
        System.out.println("  the receiver redeems it and gets " + got.length + " bytes, identical to what was sent: " + Arrays.equals(got, invoicePdf(5000)) + ".");
    }

    private static void three() {
        System.out.println("THREE. What the broker carries.");
        Broker direct = new Broker(Integer.MAX_VALUE);
        Broker claims = new Broker(LIMIT);
        BlobStore store = new BlobStore(new Clock(), 60);
        Sender sender = new Sender(claims, store);
        for (int i = 0; i < 100; i++) {
            direct.publish(new Broker.Message("invoice", invoicePdf(5000)));
            sender.send("invoice", invoicePdf(5000));
        }
        System.out.println("  100 invoices of 5000 bytes. through a broker with no limit: " + direct.bytesCarried() + " bytes. by claim: " + claims.bytesCarried() + " bytes.");
        System.out.println("  the broker moves a small ticket. the storage holds the luggage.");
    }

    private static void four() {
        System.out.println("FOUR. Luggage nobody collected.");
        Clock clock = new Clock();
        Broker broker = new Broker(LIMIT);
        BlobStore store = new BlobStore(clock, 60);
        Sender sender = new Sender(broker, store);
        for (int i = 0; i < 10; i++) {
            sender.send("invoice", invoicePdf(5000));
        }
        Receiver receiver = new Receiver(broker, store);
        for (int i = 0; i < 6; i++) {
            receiver.receive();
        }
        System.out.println("  10 sent, 6 collected and deleted. blobs still stored: " + store.stored() + ".");
        clock.advance(61);
        System.out.println("  after the time limit, the sweep removes " + store.deleteExpired() + ". stored now: " + store.stored() + ".");
        try {
            receiver.receive();
        } catch (BlobStore.ClaimExpired e) {
            System.out.println("  a slow receiver arrives with its claim: " + e.getMessage() + ".");
        }
    }

    private static void five() {
        System.out.println("FIVE. Is it the same luggage?");
        Broker broker = new Broker(LIMIT);
        BlobStore store = new BlobStore(new Clock(), 60);
        Claim claim = new Sender(broker, store).send("invoice", invoicePdf(5000));
        store.tamper(claim.blobId());
        try {
            new Receiver(broker, store).receive();
        } catch (IllegalStateException e) {
            System.out.println("  one byte changed in storage. the receiver: " + e.getMessage() + ".");
        }
        System.out.println("  the checksum in the claim is what makes a ticket for a blob safe to trust.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Broker broker = new Broker(LIMIT);
        BlobStore store = new BlobStore(new Clock(), 60);
        new Sender(broker, store).send("invoice", invoicePdf(5000));
        new Receiver(broker, store).receive();
        System.out.println("  one invoice, one way: " + store.operations() + " storage operations (put, get, delete) and 2 broker steps. before, there was 1.");
        BlobStore counting = new BlobStore(new Clock(), 60, BlobStore.sequential());
        counting.put("ada's invoice".getBytes());
        counting.put("ben's invoice".getBytes());
        System.out.println("  claims that count up: someone holding blob-1 tries blob-2 and reads: " + new String(counting.get("blob-2")) + ".");
        BlobStore random = new BlobStore(new Clock(), 60);
        random.put("ada's invoice".getBytes());
        int hits = 0;
        for (int i = 1; i <= 100_000; i++) {
            try {
                random.get("blob-" + i);
                hits++;
            } catch (BlobStore.ClaimExpired e) {
                // not a real claim
            }
        }
        System.out.println("  random claims: 100000 guesses of the counting kind found " + hits + " invoices. a claim must be hard to guess.");
        System.out.println("  storing, then sending, can stop between the two, and leave luggage nobody has a ticket for.");
    }
}
