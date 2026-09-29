package com.jk.explore.halfsync;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

/**
 * The pattern: a fast asynchronous half that only accepts, a queue in the middle, and a synchronous half of plain worker threads.
 *
 * <p>The async half runs on the event thread and never blocks: it puts the
 * order in the queue and is ready for the next. The sync half is a few
 * ordinary threads that take orders from the queue and run blocking,
 * step-by-step code.
 */
public final class HalfSyncHalfAsync {

    private final ExecutorService eventThread = Executors.newSingleThreadExecutor();
    private final BlockingQueue<String> queue;
    private final List<Thread> workers = new ArrayList<>();
    private final OrderWork work = new OrderWork();
    private final AtomicLong worstAcceptMs = new AtomicLong();
    private final AtomicInteger peakQueue = new AtomicInteger();
    private final AtomicInteger turnedAway = new AtomicInteger();

    public HalfSyncHalfAsync(int workerCount, int queueCapacity) {
        queue = new ArrayBlockingQueue<>(queueCapacity);
        for (int i = 0; i < workerCount; i++) {
            Thread t = new Thread(this::workLoop, "worker-" + (i + 1));
            t.setDaemon(true);
            workers.add(t);
        }
    }

    public void startWorkers() {
        workers.forEach(Thread::start);
    }

    /** The synchronous half: plain blocking code, one order at a time per worker. */
    private void workLoop() {
        while (true) {
            try {
                work.process(queue.take());
            } catch (InterruptedException e) {
                return;
            }
        }
    }

    /** The asynchronous half: accept and queue, never block. */
    public void burst(int orders) throws InterruptedException {
        long arrived = System.nanoTime();
        for (int i = 1; i <= orders; i++) {
            String id = "ORD-" + i;
            eventThread.submit(() -> {
                if (queue.offer(id)) {
                    peakQueue.accumulateAndGet(queue.size(), Math::max);
                } else {
                    turnedAway.incrementAndGet();
                }
                worstAcceptMs.accumulateAndGet((System.nanoTime() - arrived) / 1_000_000, Math::max);
            });
        }
        eventThread.shutdown();
        eventThread.awaitTermination(5, TimeUnit.SECONDS);
    }

    public void awaitDone(int expected, long timeoutMs) throws InterruptedException {
        long end = System.currentTimeMillis() + timeoutMs;
        while (work.done() < expected && System.currentTimeMillis() < end) {
            Thread.sleep(5);
        }
    }

    public void stop() {
        workers.forEach(Thread::interrupt);
    }

    public long worstAcceptMs() {
        return worstAcceptMs.get();
    }

    public int peakQueue() {
        return peakQueue.get();
    }

    public int turnedAway() {
        return turnedAway.get();
    }

    public int done() {
        return work.done();
    }
}
