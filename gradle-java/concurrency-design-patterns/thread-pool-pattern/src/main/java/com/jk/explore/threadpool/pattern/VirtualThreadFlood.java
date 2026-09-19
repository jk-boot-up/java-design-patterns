package com.jk.explore.threadpool.pattern;

import com.jk.explore.threadpool.harness.Gate;

/**
 * <strong>Java's answer to the cost measured in {@code ThreadPerOrderPacking}.</strong>
 * A virtual thread (Java 21) is not a lighter platform thread — it does not
 * hold a dedicated OS thread or a fixed-size stack the whole time it is
 * alive, only while it is actually running unblocked code, which is why
 * creating a hundred thousand of them costs nothing like the platform-thread
 * number this project measures in act one.
 *
 * <p><strong>This does not retire the pool.</strong> A pool bounds a
 * resource — a database's connection limit, a downstream service's
 * concurrency limit, this project's own packing-team headcount — and a
 * virtual thread does nothing about any of those; a million virtual
 * threads all trying to open a connection to a pool of ten still queue
 * for ten connections. What virtual threads retire is the older argument
 * *for* pooling threads specifically to avoid their creation cost, for
 * work that spends most of its time blocked on I/O rather than genuinely
 * needing to run concurrently.
 */
public final class VirtualThreadFlood {

    private VirtualThreadFlood() {
    }

    public record FloodResult(int threadsCreated, long totalCreateNanos, double avgCreateMicros) {
    }

    /**
     * Creates {@code count} virtual threads, each parked on the same
     * {@link Gate}, and measures how long creating them took — directly
     * comparable to {@link com.jk.explore.threadpool.naive.ThreadPerOrderPacking#floodSafely}.
     */
    public static FloodResult floodSafely(int count, Gate releaseGate) {
        long start = System.nanoTime();
        Thread[] threads = new Thread[count];
        for (int i = 0; i < count; i++) {
            threads[i] = Thread.ofVirtual().unstarted(releaseGate::awaitOpen);
            threads[i].start();
        }
        long created = System.nanoTime() - start;
        releaseGate.open();
        for (Thread t : threads) {
            try {
                t.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new IllegalStateException("interrupted joining flood threads", e);
            }
        }
        return new FloodResult(count, created, (created / 1000.0) / count);
    }
}
