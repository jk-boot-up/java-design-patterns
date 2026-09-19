package com.jk.explore.monitorobject.naive;

import java.util.concurrent.locks.ReentrantLock;

/**
 * <strong>The lock lives outside the object.</strong> Every caller is meant
 * to take {@link #lock()} before calling {@link #sellOne()}. Nothing makes
 * them. Four careful call sites protect nothing if a fifth forgets.
 */
public class CallerLockedStock {

    private final ReentrantLock lock = new ReentrantLock();
    private int count;
    private final Runnable betweenReadAndWrite;

    public CallerLockedStock(int initial, Runnable betweenReadAndWrite) {
        this.count = initial;
        this.betweenReadAndWrite = betweenReadAndWrite;
    }

    public ReentrantLock lock() {
        return lock;
    }

    public void sellOne() {
        int seen = count;
        betweenReadAndWrite.run();
        count = seen - 1;
    }

    public int available() {
        return count;
    }
}
