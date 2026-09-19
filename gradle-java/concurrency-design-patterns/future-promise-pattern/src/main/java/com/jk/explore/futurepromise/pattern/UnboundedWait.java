package com.jk.explore.futurepromise.pattern;

import com.jk.explore.futurepromise.harness.Gate;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * <strong>{@code get()} with no timeout is a hang.</strong> A task that
 * never completes — here, one parked forever on a {@link Gate} nobody
 * opens — leaves a bare {@code future.get()} blocked for as long as the
 * calling thread is willing to wait, which by default is forever. The
 * {@code timeoutMillis} argument below is not the task's patience; it is
 * the only thing standing between this demonstration and an actual hang.
 */
public final class UnboundedWait {

    private UnboundedWait() {
    }

    public record Outcome(boolean timedOut, long waitedMillis) {
    }

    public static Outcome attemptGet(ExecutorService pool, Gate neverOpened, long timeoutMillis) {
        long start = System.nanoTime();
        Future<Void> future = pool.submit(() -> {
            neverOpened.awaitOpen();
            return null;
        });

        boolean timedOut;
        try {
            future.get(timeoutMillis, TimeUnit.MILLISECONDS);
            timedOut = false;
        } catch (TimeoutException e) {
            timedOut = true;
        } catch (Exception e) {
            throw new IllegalStateException("unexpected failure waiting on the future", e);
        } finally {
            future.cancel(true);
        }
        long waitedMillis = (System.nanoTime() - start) / 1_000_000;
        return new Outcome(timedOut, waitedMillis);
    }
}
