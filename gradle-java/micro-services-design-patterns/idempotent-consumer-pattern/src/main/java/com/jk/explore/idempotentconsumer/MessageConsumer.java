package com.jk.explore.idempotentconsumer;

/** Anything that can be given a message. Implemented four different ways in this project. */
public interface MessageConsumer {

    /** The name that appears in the timeline. */
    String name();

    /** Handles one message, which may well be one it has already handled. */
    void handle(Message message);
}
