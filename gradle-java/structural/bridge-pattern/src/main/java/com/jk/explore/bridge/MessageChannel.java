package com.jk.explore.bridge;

/**
 * The Implementor. Knows how to deliver a subject/body pair somewhere --
 * and nothing about what kind of notification it is delivering.
 */
public interface MessageChannel {

    String channelName();

    void deliver(String recipient, String subject, String body);
}
