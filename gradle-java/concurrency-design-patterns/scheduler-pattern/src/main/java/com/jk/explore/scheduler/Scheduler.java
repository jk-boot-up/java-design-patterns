package com.jk.explore.scheduler;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

/**
 * The pattern: threads ask the scheduler for their turn at a shared resource, and a replaceable policy decides whose turn is next.
 *
 * <p>{@link #enter} blocks until the resource is free and the policy picks
 * this job; {@link #done} frees it. The policy is just a comparator, so
 * "express first" or "smallest first" is a one-line change.
 */
public final class Scheduler {

    private final ReentrantLock lock = new ReentrantLock();
    private final Condition changed = lock.newCondition();
    private final List<PrintJob> waiting = new ArrayList<>();
    private final Comparator<PrintJob> policy;
    private final int promoteAfter;
    private boolean busy;

    public Scheduler(Comparator<PrintJob> policy) {
        this(policy, Integer.MAX_VALUE);
    }

    /** A job passed over {@code promoteAfter} times goes to the front: nobody waits for ever. */
    public Scheduler(Comparator<PrintJob> policy, int promoteAfter) {
        this.policy = policy;
        this.promoteAfter = promoteAfter;
    }

    public void enter(PrintJob job) throws InterruptedException {
        lock.lock();
        try {
            waiting.add(job);
            while (busy || next() != job) {
                changed.await();
            }
            waiting.remove(job);
            // every job that arrived earlier and was overtaken counts one more pass
            waiting.stream().filter(w -> w.arrived() < job.arrived()).forEach(w -> w.passedOver++);
            busy = true;
        } finally {
            lock.unlock();
        }
    }

    public void done() {
        lock.lock();
        try {
            busy = false;
            changed.signalAll();
        } finally {
            lock.unlock();
        }
    }

    private PrintJob next() {
        Comparator<PrintJob> starvedFirst = Comparator.comparing((PrintJob j) -> j.passedOver < promoteAfter);
        return waiting.stream().min(starvedFirst.thenComparing(policy)).orElse(null);
    }

    public static final Comparator<PrintJob> EXPRESS_FIRST =
            Comparator.comparing((PrintJob j) -> !j.express()).thenComparingLong(PrintJob::arrived);

    public static final Comparator<PrintJob> SMALLEST_FIRST =
            Comparator.comparingInt(PrintJob::labels).thenComparingLong(PrintJob::arrived);
}
