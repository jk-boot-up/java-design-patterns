package com.jk.explore.spacehazelcast;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * The shop's database, standing in for a real one: every write takes 5 ms, one at a time.
 */
public final class SlowDatabase {

    private int stock = 1000;
    private final AtomicInteger writes = new AtomicInteger();

    public synchronized void sellOne() {
        pause();
        stock--;
        writes.incrementAndGet();
    }

    public synchronized void store(int value) {
        pause();
        stock = value;
        writes.incrementAndGet();
    }

    public synchronized int stock() {
        return stock;
    }

    public int writes() {
        return writes.get();
    }

    private static void pause() {
        try {
            Thread.sleep(5);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
