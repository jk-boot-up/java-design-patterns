package com.jk.explore.objectpool.bench;

import java.util.ArrayDeque;
import java.util.Arrays;

/**
 * <strong>Pooling a three-field object, against simply allocating one.</strong>
 * A hand-rolled measurement, so its method is written down. It is not JMH, and
 * the numbers vary by machine. The direction, and the reasons, are the claim.
 *
 * <p>Method: each variant does the same work per operation (fill a receipt, add
 * its total to a running sum that is read at the end, so the work cannot be
 * optimised away). The pool is a synchronised {@link ArrayDeque}, the simplest
 * thread-safe pool there is. There are warm-up rounds that are discarded, then
 * several measured rounds, and the <em>median</em> per-operation time is
 * reported. The variants alternate, so none always runs first. Allocation is
 * measured twice: once as plain code, where the JIT may remove it entirely, and
 * once with the object stored in a static field, so it cannot be removed.
 */
public final class SmallObjectBenchmark {

    public static final int OPERATIONS = 20_000_000;
    public static final int WARMUP_ROUNDS = 5;
    public static final int MEASURED_ROUNDS = 9;

    private static volatile long sink;

    private SmallObjectBenchmark() {
    }

    /**
     * Per-operation times in nanoseconds. {@code allocateNanosPerOp} lets the JIT see
     * the object never escapes, so it may not allocate at all. {@code allocateEscapingNanosPerOp}
     * stores every object in a static field, so a real heap allocation must happen.
     */
    public record Result(double allocateNanosPerOp, double allocateEscapingNanosPerOp, double poolNanosPerOp) {
        public double poolIsSlowerThanEscapingAllocationBy() {
            return poolNanosPerOp / allocateEscapingNanosPerOp;
        }
    }

    private static Receipt escaped;

    public static Result run() {
        return run(OPERATIONS, WARMUP_ROUNDS, MEASURED_ROUNDS);
    }

    public static Result run(int operations, int warmup, int rounds) {
        Pool pool = new Pool(4);
        for (int i = 0; i < warmup; i++) {
            allocate(operations);
            allocateEscaping(operations);
            pooled(operations, pool);
        }
        double[] allocate = new double[rounds];
        double[] escaping = new double[rounds];
        double[] pooled = new double[rounds];
        for (int i = 0; i < rounds; i++) {
            long a = allocate(operations);
            long e = allocateEscaping(operations);
            long p = pooled(operations, pool);
            allocate[i] = (double) a / operations;
            escaping[i] = (double) e / operations;
            pooled[i] = (double) p / operations;
        }
        return new Result(median(allocate), median(escaping), median(pooled));
    }

    /** Objects created by the allocating variant for a run of this size: one per operation. */
    public static long objectsCreatedByAllocating(int operations) {
        return operations;
    }

    /** Objects created by the pooling variant for a run of this size: the pool's fixed few. */
    public static long objectsCreatedByPooling() {
        return 4;
    }

    private static long allocate(int operations) {
        long sum = 0;
        long start = System.nanoTime();
        for (int i = 0; i < operations; i++) {
            Receipt r = new Receipt();
            r.fill(i);
            sum += r.total();
        }
        long elapsed = System.nanoTime() - start;
        sink = sum;
        return elapsed;
    }

    private static long allocateEscaping(int operations) {
        long sum = 0;
        long start = System.nanoTime();
        for (int i = 0; i < operations; i++) {
            Receipt r = new Receipt();
            r.fill(i);
            sum += r.total();
            escaped = r;
        }
        long elapsed = System.nanoTime() - start;
        sink = sum;
        return elapsed;
    }

    private static long pooled(int operations, Pool pool) {
        long sum = 0;
        long start = System.nanoTime();
        for (int i = 0; i < operations; i++) {
            Receipt r = pool.borrow();
            r.fill(i);
            sum += r.total();
            pool.giveBack(r);
        }
        long elapsed = System.nanoTime() - start;
        sink = sum;
        return elapsed;
    }

    private static double median(double[] values) {
        double[] sorted = values.clone();
        Arrays.sort(sorted);
        return sorted[sorted.length / 2];
    }

    /** The simplest thread-safe pool: one lock around a deque. */
    private static final class Pool {

        private final ArrayDeque<Receipt> idle = new ArrayDeque<>();

        Pool(int size) {
            for (int i = 0; i < size; i++) {
                idle.add(new Receipt());
            }
        }

        synchronized Receipt borrow() {
            Receipt r = idle.poll();
            return r != null ? r : new Receipt();
        }

        synchronized void giveBack(Receipt r) {
            r.clear();
            idle.add(r);
        }
    }
}
