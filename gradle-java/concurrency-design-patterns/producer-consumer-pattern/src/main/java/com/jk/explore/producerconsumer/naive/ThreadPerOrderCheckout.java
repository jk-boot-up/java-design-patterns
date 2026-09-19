package com.jk.explore.producerconsumer.naive;

import com.jk.explore.producerconsumer.domain.Order;
import com.jk.explore.producerconsumer.domain.Packing;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * <strong>The second naive version, and the one most people reach for
 * first.</strong> Checkout hands each order to a brand new thread and
 * returns immediately. It works — the shopper is not held up — until
 * arrivals outpace packing, at which point there is no brake anywhere:
 * every order in flight is a live thread, holding a stack, until packing
 * catches up.
 *
 * <p><strong>This class never actually exhausts the machine it runs on.</strong>
 * {@link #floodSafely} creates a capped, small number of real threads, times
 * the creation, and extrapolates the cost of the uncapped version from real
 * numbers rather than reaching the cliff. `OutOfMemoryError: unable to
 * create native thread` is real and is named in the narration; it is not
 * triggered by this code, because a teaching demo that can wedge a laptop
 * is not a teaching demo.
 */
public final class ThreadPerOrderCheckout {

    private final Packing packing;
    private final AtomicInteger liveThreads = new AtomicInteger();

    public ThreadPerOrderCheckout(Packing packing) {
        this.packing = packing;
    }

    /** Returns immediately; packing happens on a new thread. */
    public void checkout(Order order) {
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
     * Creates {@code count} real threads (each parked on a {@link com.jk.explore.producerconsumer.harness.Gate}
     * rather than doing real work, so this method returns quickly and never
     * builds up unpacked orders) and measures how long creating them actually
     * took. {@code count} is a parameter precisely so a test can keep it tiny
     * and the demo can keep it merely large.
     */
    public static FloodResult floodSafely(int count,
            com.jk.explore.producerconsumer.harness.Gate releaseGate) {
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
