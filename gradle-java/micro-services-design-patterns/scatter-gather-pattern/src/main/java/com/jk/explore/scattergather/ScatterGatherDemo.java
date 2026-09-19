package com.jk.explore.scattergather;

import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ScatterGatherDemo {

    public static void main(String[] args) {
        ExecutorService pool = Executors.newCachedThreadPool();
        try {
            one();
            two();
            three(pool);
            four(pool);
            five(pool);
            six();
        } finally {
            pool.shutdownNow();
        }
    }

    private static void one() {
        System.out.println("ONE. Ask them one after another.");
        System.out.println("  four suppliers answer in " + Latencies.FOUR + " milliseconds. asked in turn, the page waits " + Latencies.sequentialTotal(Latencies.FOUR) + ".");
    }

    private static void two() {
        System.out.println("TWO. Ask them all at once.");
        System.out.println("  the same four, asked together: the page waits for the slowest, " + Latencies.parallelTotal(Latencies.FOUR) + " milliseconds.");
    }

    /** Four suppliers held at gates: how many are being asked at the same moment. */
    static int askedAtOnce(ExecutorService pool) {
        Gate gate = new Gate();
        java.util.concurrent.atomic.AtomicInteger inFlight = new java.util.concurrent.atomic.AtomicInteger();
        java.util.concurrent.atomic.AtomicInteger peak = new java.util.concurrent.atomic.AtomicInteger();
        List<Supplier> suppliers = new java.util.ArrayList<>();
        for (String n : List.of("Acme", "Beta", "Cargo", "Delta")) {
            suppliers.add(new Supplier() {
                public String name() {
                    return n;
                }

                public Quote quote(String sku) {
                    peak.accumulateAndGet(inFlight.incrementAndGet(), Math::max);
                    gate.await();
                    inFlight.decrementAndGet();
                    return new Quote(n, 1000);
                }
            });
        }
        Thread opener = new Thread(() -> {
            long until = System.nanoTime() + 10_000_000_000L;
            while (peak.get() < 4 && System.nanoTime() < until) {
                Thread.onSpinWait();
            }
            gate.open();
        });
        opener.start();
        new ScatterGather(pool).ask(suppliers, "MUG-BLUE", 5000);
        return peak.get();
    }

    private static void three(ExecutorService pool) {
        System.out.println("THREE. Do not wait for the slowest.");
        System.out.println("  four suppliers held at once, all being asked together: " + askedAtOnce(pool) + " at the same moment.");
        Gate never = new Gate();
        List<Supplier> suppliers = List.of(Supplier.fixed("Acme", 1250), Supplier.fixed("Beta", 1190), Supplier.fixed("Cargo", 1340), Supplier.held("Delta", 990, never));
        ScatterGather.Result r = new ScatterGather(pool).ask(suppliers, "MUG-BLUE", 500);
        System.out.println("  a deadline of 500 ms. quotes gathered: " + r.quotes() + ".");
        System.out.println("  missing: " + r.missing() + ". best price shown: " + r.best().supplier() + " at " + r.best().pence() + ".");
        System.out.println("  with the deadline, the page waits " + Latencies.withDeadline(Latencies.FOUR, 500) + " ms, not " + Latencies.parallelTotal(Latencies.FOUR) + ".");
        never.open();
    }

    private static void four(ExecutorService pool) {
        System.out.println("FOUR. Say what was left out.");
        Gate never = new Gate();
        List<Supplier> suppliers = List.of(Supplier.fixed("Acme", 1250), Supplier.fixed("Beta", 1190), Supplier.held("Delta", 990, never));
        ScatterGather.Result r = new ScatterGather(pool).ask(suppliers, "MUG-BLUE", 500);
        System.out.println("  the page shows: best of " + r.quotes().size() + " of " + suppliers.size() + " suppliers, " + r.best().pence() + " from " + r.best().supplier() + ".");
        System.out.println("  the one that did not answer, Delta, would have been " + 990 + ". a partial answer is honest only if it says it is partial.");
        never.open();
    }

    private static void five(ExecutorService pool) {
        System.out.println("FIVE. A supplier that fails.");
        List<Supplier> suppliers = List.of(Supplier.fixed("Acme", 1250), Supplier.failing("Beta"), Supplier.fixed("Cargo", 1340));
        ScatterGather.Result r = new ScatterGather(pool).ask(suppliers, "MUG-BLUE", 500);
        System.out.println("  Beta is down. quotes: " + r.quotes() + ". missing: " + r.missing() + ".");
        System.out.println("  one failure did not fail the page.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        System.out.println("  one page view is now 4 supplier calls. 1000 page views: " + 1000 * 4 + " calls, to suppliers who see only the traffic, not the pages.");
        for (int n : new int[]{1, 4, 10}) {
            System.out.println("  if each supplier is quick 99 times in 100, asking " + n + " and waiting for all means " + String.format("%.1f", Latencies.chanceAllFast(n)) + " in 100 pages are quick.");
        }
        System.out.println("  the more you ask, the more often the slowest one sets the pace. a deadline is what stops it.");
    }
}
