package com.jk.explore.readwritelock.naive;

import com.jk.explore.readwritelock.domain.Price;

import java.util.concurrent.locks.ReentrantLock;

/**
 * <strong>The obvious fix, and it is correct.</strong> One mutual-exclusion
 * lock guards both {@link #read} and {@link #write} — no torn read is
 * possible, because a reader and a writer can never run at the same
 * moment. The cost this class exists to show: two readers cannot possibly
 * interfere with each other, and this lock makes them queue behind each
 * other anyway, because it cannot tell the difference between a reader
 * and a writer at all.
 */
public final class SingleLockCatalogue {

    private final ReentrantLock lock = new ReentrantLock();
    private Price price;

    public SingleLockCatalogue(Price initial) {
        this.price = initial;
    }

    public Price read() {
        lock.lock();
        try {
            return price;
        } finally {
            lock.unlock();
        }
    }

    public void write(Price newPrice) {
        lock.lock();
        try {
            this.price = newPrice;
        } finally {
            lock.unlock();
        }
    }
}
