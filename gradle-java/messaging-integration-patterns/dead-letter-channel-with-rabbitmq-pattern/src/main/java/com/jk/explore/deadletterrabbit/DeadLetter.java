package com.jk.explore.deadletterrabbit;

/**
 * An order the broker took out of the working queue, together with the note the broker wrote about it.
 * The reason is the broker's own word for why the order died: rejected, expired or maxlen.
 */
public record DeadLetter(String id, String body, String reason, String fromQueue, long count) {
}
