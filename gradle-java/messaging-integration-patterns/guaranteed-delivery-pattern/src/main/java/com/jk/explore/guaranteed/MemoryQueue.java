package com.jk.explore.guaranteed;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * Without the pattern: queued messages live only in memory, so a crash or a restart loses them all.
 */
public final class MemoryQueue {

    private final Deque<String> messages = new ArrayDeque<>();

    public void send(String message) {
        messages.add(message);
    }

    public String take() {
        return messages.poll();
    }

    public int size() {
        return messages.size();
    }
}
