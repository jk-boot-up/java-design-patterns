package com.jk.explore.halfsync;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Without the pattern: the event thread that receives orders also does each order's blocking work.
 *
 * <p>While it charges one card, it cannot even accept the next order.
 */
public final class EventThreadOnly {

    private final ExecutorService eventThread = Executors.newSingleThreadExecutor();
    private final AtomicLong worstAcceptMs = new AtomicLong();
    private final OrderWork work = new OrderWork();

    public void burst(int orders) throws InterruptedException {
        long arrived = System.nanoTime();
        for (int i = 1; i <= orders; i++) {
            String id = "ORD-" + i;
            eventThread.submit(() -> {
                worstAcceptMs.accumulateAndGet((System.nanoTime() - arrived) / 1_000_000, Math::max);
                work.process(id);
            });
        }
        eventThread.shutdown();
        eventThread.awaitTermination(30, TimeUnit.SECONDS);
    }

    public long worstAcceptMs() {
        return worstAcceptMs.get();
    }

    public int done() {
        return work.done();
    }
}
