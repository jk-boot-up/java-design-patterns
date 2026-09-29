package com.jk.explore.hedgedrequests;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: the slow tail, hedging after a delay, hedging at once, a real race with cancellation, and the bill.
 */
public final class HedgedRequestsDemo {

    static final int REQUESTS = 1000;

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. One call per price, and a slow tail.");
        LatencyModel.Stats none = LatencyModel.simulate(REQUESTS, -1);
        out.add("  " + REQUESTS + " price lookups: median " + none.p50() + " ms, 99th percentile " + none.p99() + " ms");
        out.add("  about 1 call in 33 hits a paused replica, and the product page waits a whole second");

        out.add("");
        out.add("TWO. Hedge: if no answer in 50 ms, ask a second replica.");
        LatencyModel.Stats hedged = LatencyModel.simulate(REQUESTS, 50);
        out.add("  median " + hedged.p50() + " ms, 99th percentile " + hedged.p99() + " ms, worst " + hedged.worst() + " ms");
        out.add("  extra calls: " + hedged.extraCalls() + " of " + REQUESTS + " (" + percent(hedged.extraCalls()) + ")");

        out.add("");
        out.add("THREE. Hedge at once: always ask two replicas.");
        LatencyModel.Stats both = LatencyModel.simulate(REQUESTS, 0);
        out.add("  99th percentile " + both.p99() + " ms, but extra calls: " + both.extraCalls() + " of " + REQUESTS
                + " (" + percent(both.extraCalls()) + ")");
        out.add("  twice the load for 50 ms less: waiting first is the better deal");

        out.add("");
        out.add("FOUR. A real race, with real threads.");
        Replica paused = new Replica("replica A", 1000);
        Replica healthy = new Replica("replica B", 20);
        try (Hedger hedger = new Hedger()) {
            long start = System.nanoTime();
            String answer = hedger.call(paused.price("MUG-1"), healthy.price("MUG-1"), 50);
            long millis = (System.nanoTime() - start) / 1_000_000;
            out.add("  answer: " + answer);
            out.add("  time: " + (millis < 500 ? "under 0.5 s" : "over 0.5 s") + ", not the 1 s replica A needed");
            Thread.sleep(50);
            out.add("  replica A's call cancelled: " + paused.wasCancelled());
        }

        out.add("");
        out.add("FIVE. The bill: only safe to repeat, and only when load is low.");
        out.add("  hedge price lookups, never \"place order\": two calls could charge twice");
        out.add("  if every replica is slow from overload, hedging adds load: cap hedges at a few percent");
        return out;
    }

    private static String percent(int calls) {
        return (calls * 100 / REQUESTS) + "%";
    }

    private HedgedRequestsDemo() {
    }
}
