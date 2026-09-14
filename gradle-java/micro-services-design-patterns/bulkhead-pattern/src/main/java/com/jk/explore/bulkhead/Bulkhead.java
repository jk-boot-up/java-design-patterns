package com.jk.explore.bulkhead;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.Callable;
import java.util.concurrent.Future;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * A named, bounded pot of threads that one kind of work is allowed to use.
 *
 * There is almost nothing to this class, which is worth saying out loud: a bulkhead
 * is not a clever algorithm, it is a decision to stop sharing. The mechanism is a
 * fixed thread pool with a bounded queue, and the pattern is in <em>having two of
 * them</em> rather than in anything either one does.
 *
 * <p>Two choices in here are the ones that matter:
 *
 * <p><strong>The queue is bounded.</strong> An unbounded queue never refuses
 * anything, which sounds generous and is not: jobs pile up until memory runs out,
 * and callers wait for work that will not start for minutes.
 *
 * <p><strong>A full bulkhead refuses immediately.</strong> The caller finds out in a
 * millisecond, and can do something else — degrade, shed the request, try later.
 * That is the same idea as the circuit breaker's fast failure, applied to a queue
 * rather than to a broken service.
 */
public final class Bulkhead implements AutoCloseable {

    private final String name;
    private final ThreadPoolExecutor pool;
    private final JobLog log;
    private final AtomicInteger rejected = new AtomicInteger();
    private final AtomicInteger accepted = new AtomicInteger();

    /**
     * @param threads how many jobs can run at once
     * @param queueCapacity how many may wait; beyond this, jobs are refused
     */
    public Bulkhead(String name, int threads, int queueCapacity, JobLog log) {
        this.name = name;
        this.log = log;
        this.pool = new ThreadPoolExecutor(threads, threads, 0L, TimeUnit.MILLISECONDS,
                new ArrayBlockingQueue<>(queueCapacity),
                runnable -> new Thread(runnable, name + "-worker"));
    }

    /**
     * Runs a job on this bulkhead's threads.
     *
     * @throws BulkheadFullException at once, if every thread is busy and the queue is
     *         full
     */
    public <T> Future<T> submit(String jobName, Callable<T> job) {
        try {
            Future<T> future = pool.submit(() -> {
                log.note(name, jobName, "started on " + Thread.currentThread().getName());
                T answer = job.call();
                log.note(name, jobName, "finished");
                return answer;
            });
            accepted.incrementAndGet();
            return future;
        } catch (RejectedExecutionException full) {
            rejected.incrementAndGet();
            log.note(name, jobName, "REFUSED: bulkhead full");
            throw new BulkheadFullException(name);
        }
    }

    public String name() {
        return name;
    }

    /** How many threads this bulkhead owns, busy or not. */
    public int size() {
        return pool.getMaximumPoolSize();
    }

    /** How many of its threads are working right now. */
    public int busyThreads() {
        return pool.getActiveCount();
    }

    /** How many threads it owns that have nothing to do. This is the cost of the pattern. */
    public int idleThreads() {
        return size() - busyThreads();
    }

    public int queued() {
        return pool.getQueue().size();
    }

    public int accepted() {
        return accepted.get();
    }

    public int rejected() {
        return rejected.get();
    }

    @Override
    public void close() {
        pool.shutdownNow();
    }
}
