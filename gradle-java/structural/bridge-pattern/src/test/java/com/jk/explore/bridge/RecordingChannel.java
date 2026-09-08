package com.jk.explore.bridge;

/** A test-only Implementor that records what it was asked to deliver. */
final class RecordingChannel implements MessageChannel {

    String recipient;
    String subject;
    String body;

    @Override
    public String channelName() {
        return "Recording";
    }

    @Override
    public void deliver(String recipient, String subject, String body) {
        this.recipient = recipient;
        this.subject = subject;
        this.body = body;
    }
}
