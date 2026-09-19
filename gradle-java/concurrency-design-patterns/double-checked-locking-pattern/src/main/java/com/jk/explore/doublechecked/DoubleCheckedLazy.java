package com.jk.explore.doublechecked;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

/**
 * Check without the lock; if it looks missing, take the lock and check again. Once built, no call takes
 * the lock. The field must be volatile: without it a thread may see the reference before the object it
 * points to is fully built.
 */
public class DoubleCheckedLazy {

    public static final AtomicInteger LOCKS_TAKEN = new AtomicInteger();
    private static final ReentrantLock LOCK = new ReentrantLock();
    private static volatile PriceList instance;

    private DoubleCheckedLazy() {
    }

    public static PriceList get() {
        PriceList local = instance;
        if (local == null) {
            Rendezvous.meet();
            LOCK.lock();
            LOCKS_TAKEN.incrementAndGet();
            try {
                local = instance;
                if (local == null) {
                    local = new PriceList();
                    instance = local;
                }
            } finally {
                LOCK.unlock();
            }
        }
        return local;
    }

    public static void reset() {
        instance = null;
        LOCKS_TAKEN.set(0);
    }
}
