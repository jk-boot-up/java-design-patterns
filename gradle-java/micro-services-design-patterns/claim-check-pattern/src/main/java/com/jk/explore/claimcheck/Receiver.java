package com.jk.explore.claimcheck;

/** Takes a claim off the broker, redeems it for the payload, checks it, and lets the storage go. */
public class Receiver {

    private final Broker broker;
    private final BlobStore store;

    public Receiver(Broker broker, BlobStore store) {
        this.broker = broker;
        this.store = store;
    }

    public byte[] receive() {
        Broker.Message m = broker.receive();
        Claim claim = Claim.fromBytes(m.body());
        byte[] payload = store.get(claim.blobId());
        if (!Claim.checksum(payload).equals(claim.sha256())) {
            throw new IllegalStateException("the payload is not the one that was sent: the checksum does not match");
        }
        store.delete(claim.blobId());
        return payload;
    }
}
