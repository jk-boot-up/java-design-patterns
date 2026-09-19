package com.jk.explore.guardedsuspension;

import java.util.ArrayDeque;
import java.util.Queue;
import java.util.concurrent.atomic.AtomicInteger;

/** Waits by asking again and again whether an order has come. It never stops working while it waits. */
public class SpinningInbox implements Inbox {

    private final Queue<String> orders = new ArrayDeque<>();
    private final AtomicInteger checks = new AtomicInteger();

    public synchronized void put(String order) {
        orders.add(order);
    }

    public String take() {
        while (true) {
            checks.incrementAndGet();
            synchronized (this) {
                if (!orders.isEmpty()) {
                    return orders.poll();
                }
            }
        }
    }

    public int checks() {
        return checks.get();
    }

    public int wakeups() {
        return 0;
    }
}
