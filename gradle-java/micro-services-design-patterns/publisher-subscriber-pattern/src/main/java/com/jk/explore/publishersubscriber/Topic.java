package com.jk.explore.publishersubscriber;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Predicate;

/**
 * A topic: an append-only log of events, and any number of subscriptions reading it. The publisher only
 * appends. Each subscription has its own offset, its own filter and its own pace, so one being slow, or
 * absent, does not affect another.
 */
public class Topic {

    public class Subscription {
        private final String name;
        private final Predicate<Event> filter;
        private final Consumer<Event> handler;
        private int offset;
        private boolean connected = true;

        private Subscription(String name, Predicate<Event> filter, Consumer<Event> handler, int offset) {
            this.name = name;
            this.filter = filter;
            this.handler = handler;
            this.offset = offset;
        }

        public String name() {
            return name;
        }

        /** Events published that this subscription has not yet been given, whether or not it wants them. */
        public int backlog() {
            return log.size() - offset;
        }

        public void disconnect() {
            connected = false;
        }

        public void reconnect() {
            connected = true;
        }

        /** Handles up to {@code max} pending events, and returns how many it looked at. */
        public int deliver(int max) {
            int looked = 0;
            while (connected && looked < max && offset < log.size()) {
                Event e = log.get(offset++);
                looked++;
                if (filter.test(e)) {
                    handler.accept(e);
                }
            }
            return looked;
        }
    }

    private final List<Event> log = new ArrayList<>();

    public void publish(Event e) {
        log.add(e);
    }

    public int published() {
        return log.size();
    }

    /** Sees only what is published from now on. */
    public Subscription subscribeLive(String name, Predicate<Event> filter, Consumer<Event> handler) {
        return new Subscription(name, filter, handler, log.size());
    }

    /** Sees everything ever published, and then what follows. */
    public Subscription subscribeFromStart(String name, Predicate<Event> filter, Consumer<Event> handler) {
        return new Subscription(name, filter, handler, 0);
    }
}
