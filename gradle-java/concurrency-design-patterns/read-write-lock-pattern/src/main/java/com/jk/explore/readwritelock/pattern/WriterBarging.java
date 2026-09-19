package com.jk.explore.readwritelock.pattern;

import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * <strong>The mechanism behind writer starvation.</strong> A writer
 * already queued, waiting its turn, is not necessarily served next. The
 * read lock's {@code tryLock()} is documented to acquire immediately
 * whenever the write lock is free — "whether or not other threads are
 * currently waiting for the read lock" — deliberately barging past a
 * queued writer. Do this continuously under a steady stream of readers
 * and a writer can wait far longer than its own work would ever justify.
 */
public final class WriterBarging {

    private WriterBarging() {
    }

    public record Outcome(boolean writerWasQueued, boolean secondReaderBarged) {
    }

    public static Outcome demonstrate(ReentrantReadWriteLock lock) throws InterruptedException {
        lock.readLock().lock(); // reader A holds the read lock
        Thread writer = new Thread(() -> {
            lock.writeLock().lock();
            lock.writeLock().unlock();
        });
        writer.start();

        // Deterministic: wait until the writer is provably parked in the
        // lock's own wait queue, not merely started.
        while (!lock.hasQueuedThreads()) {
            Thread.onSpinWait();
        }
        boolean writerWasQueued = lock.hasQueuedThreads();

        // tryLock() is documented to barge regardless of the writer waiting.
        boolean secondReaderBarged = lock.readLock().tryLock();
        if (secondReaderBarged) {
            lock.readLock().unlock();
        }

        lock.readLock().unlock(); // release reader A -- the writer can now proceed
        writer.join();
        return new Outcome(writerWasQueued, secondReaderBarged);
    }
}
