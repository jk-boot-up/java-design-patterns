package com.jk.explore.claimcheck;

import java.util.ArrayDeque;
import java.util.Queue;

/** A message broker with a limit on the size of a message, as real ones have, and a count of the bytes it carried. */
public class Broker {

    public record Message(String subject, byte[] body) {
    }

    private final int limit;
    private final Queue<Message> queue = new ArrayDeque<>();
    private long bytesCarried;

    public Broker(int limit) {
        this.limit = limit;
    }

    public void publish(Message m) {
        if (m.body().length > limit) {
            throw new MessageTooLarge(m.body().length, limit);
        }
        bytesCarried += m.body().length;
        queue.add(m);
    }

    public Message receive() {
        return queue.poll();
    }

    public long bytesCarried() {
        return bytesCarried;
    }
}
