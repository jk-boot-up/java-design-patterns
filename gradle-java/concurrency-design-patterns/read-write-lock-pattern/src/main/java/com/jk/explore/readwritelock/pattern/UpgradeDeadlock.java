package com.jk.explore.readwritelock.pattern;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * <strong>Upgrading from a read lock to the write lock is not possible.</strong>
 * A thread holding the read lock that then calls {@code writeLock().lock()}
 * deadlocks against itself: the write lock cannot be granted while any
 * read lock is held, including its own, and that thread can never release
 * its own read lock because it is blocked trying to acquire the write
 * lock first. This is a genuine, permanent deadlock — the
 * {@code timeoutMillis} argument below is the demonstration's rescue, not
 * the lock's patience.
 */
public final class UpgradeDeadlock {

    private UpgradeDeadlock() {
    }

    public record Outcome(boolean deadlocked, long waitedMillis) {
    }

    public static Outcome attemptUpgrade(ReentrantReadWriteLock lock, long timeoutMillis) throws InterruptedException {
        long start = System.nanoTime();
        lock.readLock().lock();
        boolean acquiredWriteLock;
        try {
            acquiredWriteLock = lock.writeLock().tryLock(timeoutMillis, TimeUnit.MILLISECONDS);
            if (acquiredWriteLock) {
                lock.writeLock().unlock();
            }
        } finally {
            lock.readLock().unlock();
        }
        long waitedMillis = (System.nanoTime() - start) / 1_000_000;
        return new Outcome(!acquiredWriteLock, waitedMillis);
    }
}
