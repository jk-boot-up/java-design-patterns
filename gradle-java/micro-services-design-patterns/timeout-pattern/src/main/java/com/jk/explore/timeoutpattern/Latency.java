package com.jk.explore.timeoutpattern;

import java.util.List;

/** How long a supplier call really takes, on a day: mostly quick, sometimes slow. Numbers, not sleeps. */
public final class Latency {

    private Latency() {
    }

    /** One hundred calls: 90 near 50ms, 8 near 200ms, 2 near 2000ms. */
    public static List<Integer> aTypicalHundred() {
        java.util.ArrayList<Integer> l = new java.util.ArrayList<>();
        for (int i = 0; i < 90; i++) l.add(40 + i % 20);
        for (int i = 0; i < 8; i++) l.add(180 + i * 5);
        l.add(2000);
        l.add(2400);
        return l;
    }

    public static long succeedingWithin(List<Integer> latencies, int limit) {
        return latencies.stream().filter(ms -> ms <= limit).count();
    }
}
