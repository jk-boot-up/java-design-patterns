package com.jk.explore.bridge;

/**
 * A concrete Implementor. Push notifications show a title on the lock
 * screen and nothing else, so the body is deliberately dropped here.
 */
public final class PushChannel implements MessageChannel {

    @Override
    public String channelName() {
        return "Push";
    }

    @Override
    public void deliver(String recipient, String subject, String body) {
        System.out.println("[PUSH to " + recipient + "] " + subject);
    }
}
