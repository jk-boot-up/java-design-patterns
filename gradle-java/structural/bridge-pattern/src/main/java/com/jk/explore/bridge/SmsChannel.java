package com.jk.explore.bridge;

/**
 * A concrete Implementor. SMS has a hard length limit, so this channel
 * folds the subject and body into one line and truncates it -- a piece of
 * channel-specific behaviour that belongs here, not in any notification.
 */
public final class SmsChannel implements MessageChannel {

    static final int MAX_LENGTH = 140;

    @Override
    public String channelName() {
        return "SMS";
    }

    @Override
    public void deliver(String recipient, String subject, String body) {
        String text = subject + ": " + body;
        if (text.length() > MAX_LENGTH) {
            text = text.substring(0, MAX_LENGTH - 1) + "…";
        }
        System.out.println("[SMS to " + recipient + "] " + text);
    }
}
