package com.jk.explore.monitorobject.pattern;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

/**
 * <strong>The monitor object: the object owns its lock and its waiting.</strong>
 * Every public method takes the lock itself, so a caller cannot forget.
 * A thread that needs stock waits on the object's own condition, and a
 * thread that adds stock signals it.
 */
public class StockMonitor {

    private final ReentrantLock lock = new ReentrantLock();
    private final Condition stockAdded = lock.newCondition();
    private int count;

    public StockMonitor(int initial) {
        this.count = initial;
    }

    public void sellOne() {
        lock.lock();
        try {
            count--;
        } finally {
            lock.unlock();
        }
    }

    /** Waits until {@code wanted} items are in stock, then takes them. The wait is in a loop on purpose. */
    public void take(int wanted) throws InterruptedException {
        lock.lockInterruptibly();
        try {
            while (count < wanted) {
                stockAdded.await();
            }
            count -= wanted;
        } finally {
            lock.unlock();
        }
    }

    public void add(int amount) {
        lock.lock();
        try {
            count += amount;
            stockAdded.signalAll();
        } finally {
            lock.unlock();
        }
    }

    /**
     * Adds stock, then calls {@code listener} <em>while still holding the
     * lock</em>. That is the mistake this method exists to demonstrate.
     */
    public void addAndNotify(int amount, Runnable listener) {
        lock.lock();
        try {
            count += amount;
            stockAdded.signalAll();
            listener.run();
        } finally {
            lock.unlock();
        }
    }

    public int available() {
        lock.lock();
        try {
            return count;
        } finally {
            lock.unlock();
        }
    }

    /**
     * Moves stock to another monitor by holding this one's lock and then
     * taking the other's. {@code holdingFirst} runs in between, so a demo
     * can arrange for two opposite transfers to meet there.
     */
    public void transferOneTo(StockMonitor other, Runnable holdingFirst) throws InterruptedException {
        lock.lockInterruptibly();
        try {
            holdingFirst.run();
            other.lock.lockInterruptibly();
            try {
                count--;
                other.count++;
            } finally {
                other.lock.unlock();
            }
        } finally {
            lock.unlock();
        }
    }
}
