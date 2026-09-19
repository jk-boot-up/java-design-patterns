package com.jk.explore.threadpool.pattern;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * <strong>The deadlock a fixed pool can reach at any size.</strong> A task
 * running inside the pool submits a second task to that same pool and then
 * waits for its result. If every worker is already busy — here, because
 * the pool has exactly one and it is the one doing the waiting — the second
 * task can never be handed a worker, the wait can never end, and no amount
 * of queue capacity changes that: the bound that starves is the worker
 * count, not the queue.
 *
 * <p>This is a genuine deadlock, not a slow path — left alone it never
 * resolves. The {@code timeoutMillis} argument is not patience for the
 * pool; it is the rescue that lets a demo, and a test, observe the hang
 * and move on rather than actually hanging forever.
 */
public final class PoolStarvation {

    private PoolStarvation() {
    }

    public record Outcome(boolean starved, long waitedMillis) {
    }

    public static Outcome attemptNestedSubmit(ExecutorService pool, long timeoutMillis) {
        long start = System.nanoTime();
        Future<String> outer = pool.submit(() -> {
            Future<String> inner = pool.submit(() -> "inner task completed");
            try {
                return inner.get(timeoutMillis, TimeUnit.MILLISECONDS);
            } catch (TimeoutException e) {
                return "TIMED OUT waiting on the inner task";
            }
        });

        String result;
        try {
            result = outer.get(timeoutMillis * 2, TimeUnit.MILLISECONDS);
        } catch (Exception e) {
            throw new IllegalStateException("outer task did not resolve", e);
        }
        long waitedMillis = (System.nanoTime() - start) / 1_000_000;
        return new Outcome(result.startsWith("TIMED OUT"), waitedMillis);
    }
}
