package com.jk.explore.cqrs;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.function.Consumer;

/**
 * How a fact gets from the write side to the read side.
 *
 * In a real shop this is Kafka, or RabbitMQ, or a database's change feed. Here it is a
 * list of subscribers and a loop, because none of the reasoning about CQRS depends on
 * which one you pick.
 *
 * <p>The method that earns this class its place is {@link #holdEvents()}. Real delivery
 * is never instant: the broker has a queue, the consumer is busy, the network hiccups.
 * Holding events lets a test and a demo place an order, look at the read model while the
 * event is still in flight, and see the customer's own order missing from their own order
 * history page. That window is the honest cost of this pattern, and a project that
 * delivers events instantly would hide it.
 */
public final class EventBus {

    private final CallLog log;
    private final List<Consumer<ShopEvent>> subscribers = new ArrayList<>();
    private final Deque<ShopEvent> held = new ArrayDeque<>();
    private boolean holding;
    private int delivered;

    public EventBus(CallLog log) {
        this.log = log;
    }

    public void subscribe(Consumer<ShopEvent> subscriber) {
        subscribers.add(subscriber);
    }

    /** Publishes a fact. Delivered at once unless the bus is holding events. */
    public void publish(ShopEvent event) {
        log.note("EventBus", "PUBLISHED", event.getClass().getSimpleName());
        if (holding) {
            held.add(event);
            log.note("EventBus", "IN-FLIGHT", held.size() + " event(s) not delivered yet");
            return;
        }
        deliver(event);
    }

    /** Stops delivering, so that the staleness window can be looked at. */
    public void holdEvents() {
        holding = true;
    }

    /** Delivers everything held, oldest first, and goes back to normal. */
    public void deliverHeld() {
        holding = false;
        while (!held.isEmpty()) {
            deliver(held.poll());
        }
    }

    public int undelivered() {
        return held.size();
    }

    public int delivered() {
        return delivered;
    }

    private void deliver(ShopEvent event) {
        delivered++;
        for (Consumer<ShopEvent> subscriber : subscribers) {
            subscriber.accept(event);
        }
    }
}
