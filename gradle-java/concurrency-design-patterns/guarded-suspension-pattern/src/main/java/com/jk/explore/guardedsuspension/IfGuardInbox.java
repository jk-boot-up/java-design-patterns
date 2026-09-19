package com.jk.explore.guardedsuspension;

import java.util.ArrayDeque;
import java.util.Queue;

/** The same as WaitingInbox, with one word changed: the guard is checked with if, not while. That is the whole bug. */
public class IfGuardInbox implements Inbox {

    private final Queue<String> orders = new ArrayDeque<>();
    private int wakeups;

    public synchronized void put(String order) {
        orders.add(order);
        notifyAll();
    }

    public synchronized String take() throws InterruptedException {
        if (orders.isEmpty()) {
            wait();
            wakeups++;
        }
        return orders.poll();
    }

    public synchronized int wakeups() {
        return wakeups;
    }
}
