package com.jk.explore.guardedsuspension;

import java.util.ArrayDeque;
import java.util.Queue;

/** Always waits, without first asking whether there is already an order. A notification that came earlier is lost. */
public class NoCheckInbox implements Inbox {

    private final Queue<String> orders = new ArrayDeque<>();

    public synchronized void put(String order) {
        orders.add(order);
        notifyAll();
    }

    public synchronized String take() throws InterruptedException {
        wait();
        return orders.poll();
    }

    public int wakeups() {
        return 0;
    }
}
