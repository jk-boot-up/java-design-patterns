package com.jk.explore.hedgedrequests;

import java.util.concurrent.Callable;
import java.util.concurrent.CompletionService;
import java.util.concurrent.ExecutorCompletionService;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

/**
 * The pattern with real threads: call the primary; if it has not answered within the hedge delay,
 * call a backup too; take whichever answers first and cancel the other.
 */
public final class Hedger implements AutoCloseable {

    private final ExecutorService pool = Executors.newCachedThreadPool();
    private int hedgesSent;

    public <T> T call(Callable<T> primary, Callable<T> backup, long hedgeAfterMillis) throws Exception {
        CompletionService<T> race = new ExecutorCompletionService<>(pool);
        Future<T> first = race.submit(primary);
        Future<T> winner = race.poll(hedgeAfterMillis, TimeUnit.MILLISECONDS);
        if (winner != null) {
            return winner.get();
        }
        hedgesSent++;
        Future<T> second = race.submit(backup);
        winner = race.take();
        (winner == first ? second : first).cancel(true);   // stop the loser's work
        return winner.get();
    }

    public int hedgesSent() {
        return hedgesSent;
    }

    @Override
    public void close() {
        pool.shutdownNow();
    }
}
