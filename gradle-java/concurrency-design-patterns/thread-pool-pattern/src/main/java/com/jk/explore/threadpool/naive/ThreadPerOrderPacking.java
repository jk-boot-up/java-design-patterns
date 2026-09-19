package com.jk.explore.threadpool.naive;

import com.jk.explore.threadpool.domain.Order;
import com.jk.explore.threadpool.domain.Packing;
import com.jk.explore.threadpool.harness.Gate;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * <strong>The version with no pool at all.</strong> Every order gets its own
 * brand new thread, same as §46's naive version — this project starts from
 * the identical failure because the pool is the fix for exactly this cost,
 * seen from the packing team's side rather than checkout's.
 *
 * <p><strong>This class never actually exhausts the machine it runs on.</strong>
 * {@link #floodSafely} creates a capped, small number of real threads, times
 * the creation, and extrapolates the cost of the uncapped version from real
 * numbers rather than reaching the cliff.
 */
public final class ThreadPerOrderPacking {

    private final Packing packing;
    private final AtomicInteger liveThreads = new AtomicInteger();

    public ThreadPerOrderPacking(Packing packing) {
        this.packing = packing;
    }

    /** Returns immediately; packing happens on a new thread. */
    public void submit(Order order) {
        liveThreads.incrementAndGet();
        Thread thread = new Thread(() -> {
            try {
                packing.pack(order);
            } finally {
                liveThreads.decrementAndGet();
            }
        });
        thread.start();
    }

    public int liveThreads() {
        return liveThreads.get();
    }

    public record FloodResult(int threadsCreated, long totalCreateNanos, double avgCreateMicros) {
    }

    /**
     * Creates {@code count} real platform threads (each parked on a
     * {@link Gate} rather than doing real work) and measures how long
     * creating them actually took. Compared directly, later, against
     * {@link com.jk.explore.threadpool.pattern.VirtualThreadFlood#floodSafely}.
     */
    public static FloodResult floodSafely(int count, Gate releaseGate) {
        long start = System.nanoTime();
        Thread[] threads = new Thread[count];
        for (int i = 0; i < count; i++) {
            threads[i] = new Thread(releaseGate::awaitOpen);
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
