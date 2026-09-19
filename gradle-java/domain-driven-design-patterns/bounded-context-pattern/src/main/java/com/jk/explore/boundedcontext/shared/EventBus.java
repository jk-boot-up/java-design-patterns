package com.jk.explore.boundedcontext.shared;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.function.Consumer;

/** A queue between contexts. Nothing is delivered until {@link #deliver()} is called, so the gap can be seen. */
public class EventBus {

    private final Queue<CustomerRenamed> queue = new ArrayDeque<>();
    private final List<Consumer<CustomerRenamed>> subscribers = new ArrayList<>();

    public void subscribe(Consumer<CustomerRenamed> subscriber) {
        subscribers.add(subscriber);
    }

    public void publish(CustomerRenamed event) {
        queue.add(event);
    }

    public int waiting() {
        return queue.size();
    }

    public void deliver() {
        while (!queue.isEmpty()) {
            CustomerRenamed event = queue.poll();
            subscribers.forEach(s -> s.accept(event));
        }
    }
}
