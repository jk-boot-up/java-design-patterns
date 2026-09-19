package com.jk.explore.guardedsuspension;

import java.util.ArrayDeque;
import java.util.Queue;

/**
 * Waits properly. The guard, is there an order?, is checked in a loop around wait(): a woken thread checks again, because
 * someone else may have taken the order, and a thread that arrives after the order is already there never waits at all.
 */
public class WaitingInbox implements Inbox {

    private final Queue<String> orders = new ArrayDeque<>();
    private int wakeups;

    public synchronized void put(String order) {
        orders.add(order);
        notifyAll();
    }

    public synchronized String take() throws InterruptedException {
        while (orders.isEmpty()) {
            wait();
            wakeups++;
        }
        return orders.poll();
    }

    /** As take(), but gives up after a while and says so by returning null. */
    public synchronized String take(long millis) throws InterruptedException {
        long deadline = System.nanoTime() + millis * 1_000_000;
        while (orders.isEmpty()) {
            long left = (deadline - System.nanoTime()) / 1_000_000;
            if (left <= 0) {
                return null;
            }
            wait(left);
        }
        return orders.poll();
    }

    public synchronized int wakeups() {
        return wakeups;
    }
}
