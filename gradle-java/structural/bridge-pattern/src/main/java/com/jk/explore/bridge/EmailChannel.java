package com.jk.explore.bridge;

/** A concrete Implementor. Delivers the full subject and body, unchanged. */
public final class EmailChannel implements MessageChannel {

    @Override
    public String channelName() {
        return "Email";
    }

    @Override
    public void deliver(String recipient, String subject, String body) {
        System.out.println("[EMAIL to " + recipient + "] " + subject + " -- " + body);
    }
}
