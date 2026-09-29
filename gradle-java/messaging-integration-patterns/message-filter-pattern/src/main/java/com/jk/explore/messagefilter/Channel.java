package com.jk.explore.messagefilter;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

/**
 * A publish-subscribe channel: every message sent is delivered to every subscriber.
 */
public final class Channel {

    private final List<Consumer<OrderEvent>> subscribers = new ArrayList<>();

    public void subscribe(Consumer<OrderEvent> subscriber) {
        subscribers.add(subscriber);
    }

    public void send(OrderEvent event) {
        subscribers.forEach(s -> s.accept(event));
    }
}
