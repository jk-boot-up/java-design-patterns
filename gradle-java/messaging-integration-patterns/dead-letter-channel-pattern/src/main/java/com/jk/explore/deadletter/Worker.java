package com.jk.explore.deadletter;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.function.Consumer;

/**
 * Takes messages one at a time from a channel and handles them. A message that fails is tried again, up to a limit,
 * and then moved to the dead letter channel with its reason, so the messages behind it can go on.
 */
public class Worker {

    private final Queue<Message> channel = new ArrayDeque<>();
    private final List<DeadLetter> deadLetters = new ArrayList<>();
    private final List<String> handled = new ArrayList<>();
    private final Consumer<Message> handler;
    private final int maxAttempts;
    private int totalAttempts;

    public Worker(Consumer<Message> handler, int maxAttempts) {
        this.handler = handler;
        this.maxAttempts = maxAttempts;
    }

    public void send(Message m) {
        channel.add(m);
    }

    /** Works through the channel. With no dead letter channel a failing message stops everything behind it. */
    public void runAll(boolean useDeadLetterChannel) {
        while (!channel.isEmpty()) {
            Message m = channel.peek();
            RuntimeException last = null;
            boolean done = false;
            for (int attempt = 1; attempt <= maxAttempts; attempt++) {
                totalAttempts++;
                try {
                    handler.accept(m);
                    done = true;
                    break;
                } catch (RuntimeException e) {
                    last = e;
                }
            }
            if (done) {
                channel.poll();
                handled.add(m.id());
            } else if (useDeadLetterChannel) {
                channel.poll();
                deadLetters.add(new DeadLetter(m, maxAttempts, last.getMessage(), "orders"));
            } else {
                return;
            }
        }
    }

    /** Puts every dead letter back on the channel, as an operator does once the cause is fixed. */
    public int replayDeadLetters() {
        int n = deadLetters.size();
        deadLetters.forEach(d -> channel.add(d.message()));
        deadLetters.clear();
        return n;
    }

    public List<String> handled() {
        return handled;
    }

    public List<DeadLetter> deadLetters() {
        return deadLetters;
    }

    public int waiting() {
        return channel.size();
    }

    public int totalAttempts() {
        return totalAttempts;
    }
}
