package com.jk.explore.doublechecked;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

/** Correct, by taking the lock on every single call. A ReentrantLock is used so the takings can be counted. */
public class SynchronisedLazy {

    public static final AtomicInteger LOCKS_TAKEN = new AtomicInteger();
    private static final ReentrantLock LOCK = new ReentrantLock();
    private static PriceList instance;

    private SynchronisedLazy() {
    }

    public static PriceList get() {
        Rendezvous.meet();
        LOCK.lock();
        LOCKS_TAKEN.incrementAndGet();
        try {
            if (instance == null) {
                instance = new PriceList();
            }
            return instance;
        } finally {
            LOCK.unlock();
        }
    }

    public static void reset() {
        instance = null;
        LOCKS_TAKEN.set(0);
    }
}
