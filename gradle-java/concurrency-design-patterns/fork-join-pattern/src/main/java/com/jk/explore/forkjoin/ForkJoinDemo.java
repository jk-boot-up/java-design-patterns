package com.jk.explore.forkjoin;

import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.atomic.AtomicInteger;

public class ForkJoinDemo {

    static final int N = 100_000;

    /** Runs the sum on a pool of {@code workers}, holding each leaf at a gate until {@code expected} leaves are running, and returns the most at once. */
    static int mostLeavesAtOnce(int workers, int leaves, int expected) {
        long[] totals = OrderTotals.generate(N);
        Gate gate = new Gate();
        AtomicInteger running = new AtomicInteger();
        AtomicInteger peak = new AtomicInteger();
        SumTask.reset();
        SumTask.ON_LEAF = () -> {
            peak.accumulateAndGet(running.incrementAndGet(), Math::max);
            long until = System.nanoTime() + 10_000_000_000L;
            while (running.get() < expected && System.nanoTime() < until) {
                Thread.onSpinWait();
            }
            gate.open();
            gate.await();
            running.decrementAndGet();
        };
        ForkJoinPool pool = new ForkJoinPool(workers);
        try {
            pool.invoke(new SumTask(totals, 0, N, N / leaves));
        } finally {
            pool.shutdown();
            SumTask.reset();
        }
        return peak.get();
    }

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. One loop.");
        long[] totals = OrderTotals.generate(N);
        System.out.println("  adding up " + N + " order totals in a loop: " + OrderTotals.sequentialSum(totals) + " pence, on one thread.");
    }

    private static void two() {
        System.out.println("TWO. Split it until it is small.");
        long[] totals = OrderTotals.generate(N);
        SumTask.reset();
        long sum = new ForkJoinPool(4).invoke(new SumTask(totals, 0, N, 10_000));
        System.out.println("  split in halves until a piece is 10000 or fewer: " + SumTask.LEAVES.get() + " pieces added directly, " + SumTask.TASKS.get() + " tasks in all.");
        System.out.println("  the total: " + sum + ", which is the same as the loop: " + (sum == OrderTotals.sequentialSum(totals)) + ".");
    }

    private static void three() {
        System.out.println("THREE. The pieces really run together.");
        System.out.println("  a pool of 4 workers, 16 pieces, each held until 4 are running at once. most running at the same moment: " + mostLeavesAtOnce(4, 16, 4) + ".");
    }

    private static void four() {
        System.out.println("FOUR. How small is small enough.");
        for (int threshold : new int[]{100_000, 10_000, 100, 1}) {
            Splitting.Shape s = Splitting.of(N, threshold);
            System.out.println("  a piece of " + threshold + " or fewer is added directly: " + s.leaves() + " pieces, " + s.tasks() + " tasks.");
        }
        System.out.println("  one piece is just the loop. one task for every item is mostly the cost of making tasks.");
    }

    private static void five() {
        System.out.println("FIVE. Pieces that are not the same size.");
        long[] even = {25, 25, 25, 25};
        long[] skewed = {85, 5, 5, 5};
        System.out.println("  four pieces of work, costs " + java.util.Arrays.toString(even) + ": the best possible speedup on 4 workers is " + String.format("%.1f", Splitting.bestSpeedup(even)) + " times.");
        System.out.println("  costs " + java.util.Arrays.toString(skewed) + ": " + String.format("%.2f", Splitting.bestSpeedup(skewed)) + " times. the job waits for the big piece, and three workers wait for it too.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        System.out.println("  a pool of 2 workers and 8 pieces that each wait on something slow, such as a database: most running at once: " + mostLeavesAtOnce(2, 8, 2) + " of 8.");
        System.out.println("  fork-join is for work that uses the processor. a worker that waits is a worker that cannot help.");
        Splitting.Shape tiny = Splitting.of(20, 1);
        System.out.println("  and for 20 items, split to single items: " + tiny.tasks() + " tasks to add up 20 numbers. small jobs are faster in a loop.");
    }
}
