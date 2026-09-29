package com.jk.explore.hedgedrequests;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Simulated price-service replicas: 20 ms normally, 1,000 ms when a replica is paused (about 1 call in 33).
 */
public final class LatencyModel {

    public static final int FAST = 20;
    public static final int SLOW = 1000;

    /** Latency of the call to the replica chosen for attempt {@code attempt} of request {@code request}. */
    public static int latency(int request, int attempt) {
        return (request + attempt * 7) % 33 == 0 ? SLOW : FAST;
    }

    public record Stats(int p50, int p99, int worst, int extraCalls) {
    }

    /** {@code hedgeAfter} below 0 means never hedge; 0 means always send two at once. */
    public static Stats simulate(int requests, int hedgeAfter) {
        List<Integer> times = new ArrayList<>();
        int extra = 0;
        for (int i = 0; i < requests; i++) {
            int primary = latency(i, 0);
            int time = primary;
            if (hedgeAfter >= 0 && primary > hedgeAfter) {
                extra++;
                time = Math.min(primary, hedgeAfter + latency(i, 1));
            }
            times.add(time);
        }
        Collections.sort(times);
        return new Stats(times.get(requests / 2), times.get(requests * 99 / 100), times.get(requests - 1), extra);
    }

    private LatencyModel() {
    }
}
