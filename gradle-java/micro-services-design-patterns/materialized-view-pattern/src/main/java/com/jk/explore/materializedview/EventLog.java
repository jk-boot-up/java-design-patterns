package com.jk.explore.materializedview;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.function.Consumer;

/**
 * The events, in order: kept forever for replay, and delivered to the view only when deliver() is called.
 *
 * <p>Holding events back until deliver() is how the demo shows the moment
 * between something happening and the view hearing about it.
 */
public final class EventLog {

    private final List<Event> all = new ArrayList<>();
    private final Queue<Event> undelivered = new ArrayDeque<>();

    public void publish(Event e) {
        all.add(e);
        undelivered.add(e);
    }

    public int deliver(Consumer<Event> subscriber) {
        int n = 0;
        while (!undelivered.isEmpty()) {
            subscriber.accept(undelivered.poll());
            n++;
        }
        return n;
    }

    public int waiting() {
        return undelivered.size();
    }

    /** Every event since the start, for rebuilding a view from nothing. */
    public List<Event> history() {
        return List.copyOf(all);
    }
}
