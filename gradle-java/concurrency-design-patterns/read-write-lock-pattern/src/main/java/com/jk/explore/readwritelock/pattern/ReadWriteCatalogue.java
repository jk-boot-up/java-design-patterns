package com.jk.explore.readwritelock.pattern;

import com.jk.explore.readwritelock.domain.Price;

import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * <strong>The pattern.</strong> Many readers may hold the read lock at
 * once; a writer holding the write lock excludes everyone, readers and
 * other writers alike. Two readers no longer queue behind each other —
 * only a writer makes anyone wait.
 */
public final class ReadWriteCatalogue {

    private final ReentrantReadWriteLock lock = new ReentrantReadWriteLock();
    private Price price;

    public ReadWriteCatalogue(Price initial) {
        this.price = initial;
    }

    public Price read() {
        lock.readLock().lock();
        try {
            return price;
        } finally {
            lock.readLock().unlock();
        }
    }

    public void write(Price newPrice) {
        lock.writeLock().lock();
        try {
            this.price = newPrice;
        } finally {
            lock.writeLock().unlock();
        }
    }

    public ReentrantReadWriteLock lock() {
        return lock;
    }
}
