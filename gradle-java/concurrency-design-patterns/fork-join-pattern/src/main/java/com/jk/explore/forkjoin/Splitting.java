package com.jk.explore.forkjoin;

/** How a slice would be split, worked out with no threads: how many leaves, and how many tasks in all. */
public final class Splitting {

    public record Shape(int leaves, int tasks) {
    }

    private Splitting() {
    }

    public static Shape of(int size, int threshold) {
        if (size <= threshold) {
            return new Shape(1, 1);
        }
        Shape left = of(size / 2, threshold);
        Shape right = of(size - size / 2, threshold);
        return new Shape(left.leaves() + right.leaves(), left.tasks() + right.tasks() + 1);
    }

    /** With one leaf far bigger than the rest, the whole job waits for it. Returns the best speedup possible. */
    public static double bestSpeedup(long[] leafCosts) {
        long total = 0;
        long biggest = 0;
        for (long c : leafCosts) {
            total += c;
            biggest = Math.max(biggest, c);
        }
        return (double) total / biggest;
    }
}
