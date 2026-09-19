package com.jk.explore.eventbus;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

/**
 * An in-process bus. Components subscribe to a type of event, and post events without knowing who is listening.
 * A subscriber for a type also hears the subtypes. A subscriber that throws does not stop the others, and the
 * failure is recorded. An event nobody hears is posted again as a DeadEvent.
 */
public class EventBus {

    public interface Subscription {
        void cancel();
    }

    private record Entry<T>(Class<T> type, Consumer<T> handler) {
    }

    private final List<Entry<?>> entries = new ArrayList<>();
    private final List<String> failures = new ArrayList<>();
    private int deadEvents;

    public <T> Subscription subscribe(Class<T> type, Consumer<T> handler) {
        Entry<T> entry = new Entry<>(type, handler);
        entries.add(entry);
        return () -> entries.remove(entry);
    }

    public void post(Object event) {
        boolean heard = false;
        for (Entry<?> e : new ArrayList<>(entries)) {
            if (e.type().isInstance(event)) {
                heard = true;
                deliver(e, event);
            }
        }
        if (!heard && !(event instanceof DeadEvent)) {
            deadEvents++;
            post(new DeadEvent(event));
        }
    }

    @SuppressWarnings("unchecked")
    private <T> void deliver(Entry<T> e, Object event) {
        try {
            e.handler().accept((T) event);
        } catch (RuntimeException ex) {
            failures.add(event.getClass().getSimpleName() + ": " + ex.getMessage());
        }
    }

    public List<String> failures() {
        return failures;
    }

    public int deadEvents() {
        return deadEvents;
    }

    public int subscribers() {
        return entries.size();
    }

    public long subscribersOf(Class<?> eventType) {
        return entries.stream().filter(e -> e.type().isAssignableFrom(eventType)).count();
    }
}
