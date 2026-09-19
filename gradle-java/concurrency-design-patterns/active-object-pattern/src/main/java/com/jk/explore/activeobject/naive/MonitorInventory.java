package com.jk.explore.activeobject.naive;

import java.util.concurrent.locks.ReentrantLock;

/**
 * <strong>The monitor from §50, used by several callers.</strong> Correct,
 * and every caller blocks while another holds the lock. The
 * {@code slowWork} argument stands for a slow import that runs inside the
 * critical section.
 */
public class MonitorInventory {

    private final ReentrantLock lock = new ReentrantLock();
    private int stock;

    public MonitorInventory(int initial) {
        this.stock = initial;
    }

    public int reserve(int amount) {
        lock.lock();
        try {
            stock -= amount;
            return stock;
        } finally {
            lock.unlock();
        }
    }

    public void importCorrection(int correctStock, Runnable slowWork) {
        lock.lock();
        try {
            slowWork.run();
            stock = correctStock;
        } finally {
            lock.unlock();
        }
    }

    public int available() {
        lock.lock();
        try {
            return stock;
        } finally {
            lock.unlock();
        }
    }
}
