package com.jk.explore.threadpool.pattern;

import com.jk.explore.threadpool.domain.Order;
import com.jk.explore.threadpool.domain.Packing;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * <strong>The pattern.</strong> A fixed, small number of packer threads,
 * created once and reused, pulling from a queue whose capacity is chosen
 * on purpose rather than left to whatever the JDK's factory method
 * defaults to. Two bounds, both explicit: how many orders can be packed at
 * once, and how many more can be waiting.
 *
 * <p>Unlike the offer-with-a-patience-window bounded queue from §46,
 * {@link ThreadPoolExecutor#execute} has no patience of its own: the
 * moment every worker is busy and the queue
 * is full, the rejection handler runs synchronously, in the calling
 * thread, before {@code execute} returns. A patience window is something a
 * caller has to build on top, not something the pool gives for free.
 */
public final class BoundedPackingPool implements AutoCloseable {

    private final ThreadPoolExecutor executor;
    private final AtomicInteger rejected = new AtomicInteger();

    public BoundedPackingPool(int workers, int queueCapacity) {
        this.executor = new ThreadPoolExecutor(
                workers, workers,
                0L, TimeUnit.MILLISECONDS,
                new ArrayBlockingQueue<>(queueCapacity),
                (task, exec) -> rejected.incrementAndGet());
    }

    /** Submits real work: an order to pack. Rejects silently — see {@link #rejectedCount()} — once both bounds are full. */
    public void submit(Order order, Packing packing) {
        try {
            executor.execute(() -> packing.pack(order));
        } catch (RejectedExecutionException e) {
            rejected.incrementAndGet();
        }
    }

    /** Submits a bare task rather than an order — used to hold a worker parked on a {@link com.jk.explore.threadpool.harness.Gate} deterministically. */
    public void submitRaw(Runnable task) {
        try {
            executor.execute(task);
        } catch (RejectedExecutionException e) {
            rejected.incrementAndGet();
        }
    }

    public int queueDepth() {
        return executor.getQueue().size();
    }

    public int rejectedCount() {
        return rejected.get();
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
