package com.jk.explore.competingconsumers;

import java.util.concurrent.LinkedBlockingDeque;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * A queue that many consumers read from. Each message goes to exactly one consumer at a time. A consumer
 * that fails to finish gives the message back, and it is handed to another.
 */
public class Broker {

    private final LinkedBlockingDeque<Delivery> queue = new LinkedBlockingDeque<>();
    private final AtomicInteger inFlight = new AtomicInteger();
    private final AtomicInteger peakInFlight = new AtomicInteger();
    private final AtomicInteger acknowledged = new AtomicInteger();

    public void publish(int id, String body) {
        queue.addLast(new Delivery(id, body, 1));
    }

    /** Waits a short while for a message, so a consumer can notice it was told to stop. */
    public Delivery receive() throws InterruptedException {
        Delivery d = queue.pollFirst(50, TimeUnit.MILLISECONDS);
        if (d != null) {
            peakInFlight.accumulateAndGet(inFlight.incrementAndGet(), Math::max);
        }
        return d;
    }

    public void ack(Delivery d) {
        inFlight.decrementAndGet();
        acknowledged.incrementAndGet();
    }

    /** Gives the message back, at the front, to be handed to whichever consumer is free. */
    public void nack(Delivery d) {
        inFlight.decrementAndGet();
        queue.addFirst(new Delivery(d.id(), d.body(), d.attempt() + 1));
    }

    public int waiting() {
        return queue.size();
    }

    public int inFlight() {
        return inFlight.get();
    }

    public int peakInFlight() {
        return peakInFlight.get();
    }

    public int acknowledged() {
        return acknowledged.get();
    }
}
