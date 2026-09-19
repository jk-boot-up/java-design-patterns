package com.jk.explore.futurepromisespring;

import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicInteger;

/** Counts how many lookups are in flight at once, and the most there ever were. Not sleeping: a gate holds them. */
@Component
public class Flight {

    private final AtomicInteger inFlight = new AtomicInteger();
    private final AtomicInteger max = new AtomicInteger();
    private volatile Gate gate = openGate();

    public void reset(Gate newGate) {
        inFlight.set(0);
        max.set(0);
        gate = newGate;
    }

    void begin() {
        int now = inFlight.incrementAndGet();
        max.accumulateAndGet(now, Math::max);
        gate.awaitOpen();
    }

    void end() {
        inFlight.decrementAndGet();
    }

    public int maxInFlight() {
        return max.get();
    }

    public int inFlightNow() {
        return inFlight.get();
    }

    private static Gate openGate() {
        Gate g = new Gate();
        g.open();
        return g;
    }
}
