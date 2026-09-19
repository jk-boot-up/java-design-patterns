package com.jk.explore.messagechannel;

import java.util.ArrayDeque;
import java.util.Queue;

/**
 * A point-to-point channel: a named queue between one kind of sender and one kind of receiver. Each message
 * is taken by exactly one receiver. It carries one type of message, and has a limit on how many may wait.
 */
public class Channel<T> {

    private final String name;
    private final String type;
    private final int capacity;
    private final Queue<Message<T>> waiting = new ArrayDeque<>();
    private int sent;
    private int received;

    public Channel(String name, String type, int capacity) {
        this.name = name;
        this.type = type;
        this.capacity = capacity;
    }

    public void send(Message<T> message) {
        if (!message.type().equals(type)) {
            throw new WrongType(name, type, message.type());
        }
        if (waiting.size() >= capacity) {
            throw new ChannelFull(name);
        }
        waiting.add(message);
        sent++;
    }

    /** Takes the next message, or returns null if there is none. */
    public Message<T> receive() {
        Message<T> m = waiting.poll();
        if (m != null) {
            received++;
        }
        return m;
    }

    public int waiting() {
        return waiting.size();
    }

    public int sent() {
        return sent;
    }

    public int received() {
        return received;
    }
}
