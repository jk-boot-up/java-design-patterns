package com.jk.explore.claimcheck;

/** Sends a big payload by putting it in storage and sending the claim. */
public class Sender {

    private final Broker broker;
    private final BlobStore store;

    public Sender(Broker broker, BlobStore store) {
        this.broker = broker;
        this.store = store;
    }

    public Claim send(String subject, byte[] payload) {
        String id = store.put(payload);
        Claim claim = new Claim(id, payload.length, Claim.checksum(payload));
        broker.publish(new Broker.Message(subject, claim.toBytes()));
        return claim;
    }
}
