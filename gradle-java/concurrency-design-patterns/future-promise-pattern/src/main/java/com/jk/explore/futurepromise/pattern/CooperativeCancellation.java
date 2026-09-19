package com.jk.explore.futurepromise.pattern;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * <strong>Cancellation is cooperative, and may do nothing.</strong>
 * {@link Future#cancel(boolean)} with {@code true} interrupts the thread
 * running the task — it does not stop the task. A task that catches
 * {@link InterruptedException} and carries on, the way this class's own
 * task deliberately does, keeps running to completion regardless of
 * {@code cancel} ever having been called at all.
 */
public final class CooperativeCancellation {

    private CooperativeCancellation() {
    }

    public record Outcome(boolean reportedCancelled, boolean taskRanToCompletion) {
    }

    public static Outcome attempt(ExecutorService pool) {
        AtomicBoolean taskFinished = new AtomicBoolean(false);
        CountDownLatch started = new CountDownLatch(1);

        Future<?> future = pool.submit(() -> {
            started.countDown();
            // Three short, real sleeps -- each interrupt is caught and
            // ignored on purpose, the exact anti-pattern this class exists
            // to demonstrate. Bounded and real, so this always finishes on
            // its own shortly, cancelled or not.
            for (int i = 0; i < 3; i++) {
                try {
                    Thread.sleep(50);
                } catch (InterruptedException ignored) {
                    // ignored on purpose
                }
            }
            taskFinished.set(true);
        });

        // cancel(true) must not race the task's own start: cancelling before
        // the worker has picked the task up at all would simply skip running
        // it, which proves nothing about interruption being ignored. This
        // latch makes "the task is already running" a fact, not a hope.
        try {
            started.await();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("interrupted waiting for the task to start", e);
        }
        boolean reportedCancelled = future.cancel(true);

        // The task keeps running on its own thread regardless of the line
        // above; this spin-wait cannot hang, because the task's own three
        // sleeps bound how long it can possibly take.
        while (!taskFinished.get()) {
            Thread.onSpinWait();
        }

        return new Outcome(reportedCancelled, taskFinished.get());
    }
}
