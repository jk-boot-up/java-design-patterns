package com.jk.explore.producerconsumer.pattern;

import com.jk.explore.producerconsumer.domain.Order;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;

/**
 * <strong>This class is the pattern.</strong> A fixed-capacity handoff
 * point between checkout and packing. Checkout offers; packing takes; each
 * runs at its own speed, and the bound is not an implementation detail — it
 * is the whole point. A queue with no bound is the second naive version
 * again, wearing a nicer name.
 */
public final class BoundedOrderQueue {

    private final BlockingQueue<Order> queue;
    private final int capacity;

    public BoundedOrderQueue(int capacity) {
        this.capacity = capacity;
        this.queue = new ArrayBlockingQueue<>(capacity);
    }

    /** Blocks the producer if the queue is full — the "apply back-pressure" policy. */
    public void put(Order order) throws InterruptedException {
        queue.put(order);
    }

    /** Waits up to {@code timeout} for room, then gives up — the "reject" policy. */
    public boolean offer(Order order, long timeout, TimeUnit unit) throws InterruptedException {
        return queue.offer(order, timeout, unit);
    }

    public Order take() throws InterruptedException {
        return queue.take();
    }

    public int size() {
        return queue.size();
    }

    public int capacity() {
        return capacity;
    }

    public boolean isFull() {
        return queue.size() == capacity;
    }
}
