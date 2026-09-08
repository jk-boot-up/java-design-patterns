package com.jk.explore.bridge;

import java.util.Objects;

/**
 * The Abstraction. Knows what a notification says; delegates how it gets
 * delivered to whichever {@link MessageChannel} it was built with.
 */
public abstract class Notification {

    private final MessageChannel channel;

    protected Notification(MessageChannel channel) {
        this.channel = Objects.requireNonNull(channel);
    }

    public final void send(String recipient) {
        channel.deliver(recipient, subject(), body());
    }

    public final String channelName() {
        return channel.channelName();
    }

    protected abstract String subject();

    protected abstract String body();
}
