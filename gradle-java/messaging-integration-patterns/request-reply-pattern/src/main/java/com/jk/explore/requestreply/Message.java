package com.jk.explore.requestreply;

import java.util.concurrent.BlockingQueue;

/**
 * A message on a queue: its own ID, the ID of the request it answers (for replies), where to send the reply, and a body.
 */
public record Message(String id, String correlationId, BlockingQueue<Message> replyTo, String body) {
}
