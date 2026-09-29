package com.jk.explore.cas;

import java.util.concurrent.locks.LockSupport;

/**
 * Correct with a lock: only one buyer at a time may look and take. Everyone else waits in line.
 */
public final class LockedStock implements Stock {

    private int left;

    public LockedStock(int left) {
        this.left = left;
    }

    @Override
    public synchronized boolean buyOne() {
        if (left <= 0) {
            return false;
        }
        LockSupport.parkNanos(20_000);
        left--;
        return true;
    }

    @Override
    public synchronized int left() {
        return left;
    }
}
