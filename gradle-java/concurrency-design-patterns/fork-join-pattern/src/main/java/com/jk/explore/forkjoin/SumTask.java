package com.jk.explore.forkjoin;

import java.util.concurrent.RecursiveTask;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Adds up a slice of the totals. If the slice is small enough it does it at once, and that is a leaf. If not, it splits
 * the slice in two, hands one half to another worker (fork), does the other half itself, and then waits for the first (join).
 */
public class SumTask extends RecursiveTask<Long> {

    /** Every task ever created, and every leaf. */
    public static final AtomicInteger TASKS = new AtomicInteger();
    public static final AtomicInteger LEAVES = new AtomicInteger();
    /** Called by each leaf as it starts its work. A demo may use it to hold leaves. */
    public static volatile Runnable ON_LEAF = () -> { };

    private final long[] totals;
    private final int from;
    private final int to;
    private final int threshold;

    public SumTask(long[] totals, int from, int to, int threshold) {
        this.totals = totals;
        this.from = from;
        this.to = to;
        this.threshold = threshold;
        TASKS.incrementAndGet();
    }

    @Override
    protected Long compute() {
        if (to - from <= threshold) {
            LEAVES.incrementAndGet();
            ON_LEAF.run();
            long sum = 0;
            for (int i = from; i < to; i++) {
                sum += totals[i];
            }
            return sum;
        }
        int middle = (from + to) >>> 1;
        SumTask left = new SumTask(totals, from, middle, threshold);
        SumTask right = new SumTask(totals, middle, to, threshold);
        left.fork();
        long rightSum = right.compute();
        return left.join() + rightSum;
    }

    public static void reset() {
        TASKS.set(0);
        LEAVES.set(0);
        ON_LEAF = () -> { };
    }
}
