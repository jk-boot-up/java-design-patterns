package com.jk.explore.scattergather;

import java.util.List;

/** How long each supplier takes to answer, in milliseconds. Numbers, not sleeps. */
public final class Latencies {

    private Latencies() {
    }

    public static final List<Integer> FOUR = List.of(80, 120, 200, 900);

    public static int sequentialTotal(List<Integer> latencies) {
        return latencies.stream().mapToInt(Integer::intValue).sum();
    }

    public static int parallelTotal(List<Integer> latencies) {
        return latencies.stream().mapToInt(Integer::intValue).max().orElse(0);
    }

    public static int withDeadline(List<Integer> latencies, int deadline) {
        return Math.min(parallelTotal(latencies), deadline);
    }

    /** The chance that every one of n calls is fast, when each is fast 99 times in 100, as a percentage. */
    public static double chanceAllFast(int n) {
        return Math.pow(0.99, n) * 100;
    }
}
