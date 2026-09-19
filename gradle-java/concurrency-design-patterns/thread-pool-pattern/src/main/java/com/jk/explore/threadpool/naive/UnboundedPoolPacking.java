package com.jk.explore.threadpool.naive;

import com.jk.explore.threadpool.domain.Order;
import com.jk.explore.threadpool.domain.Packing;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/**
 * <strong>A fixed number of worker threads — the improvement most people
 * stop at.</strong> {@link Executors#newFixedThreadPool} looks like the
 * pattern, and the worker-thread count really is bounded. The trap is what
 * it hands those workers to pull from: an unbounded {@code LinkedBlockingQueue},
 * built in behind the factory method with no argument anywhere to change
 * it. Submitting never blocks and never rejects — the backlog just grows,
 * silently, until it is a heap dump instead of a decision.
 */
public final class UnboundedPoolPacking implements AutoCloseable {

    private final ThreadPoolExecutor executor;

    public UnboundedPoolPacking(int workers) {
        this.executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(workers);
    }

    /** Never blocks and never rejects — the whole point of this class existing. */
    public void submit(Order order, Packing packing) {
        executor.execute(() -> packing.pack(order));
    }

    /** The number of tasks queued and not yet handed to a worker. */
    public int backlog() {
        return executor.getQueue().size();
    }

    public ExecutorService raw() {
        return executor;
    }

    @Override
    public void close() {
        executor.shutdown();
        try {
            executor.awaitTermination(5, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
