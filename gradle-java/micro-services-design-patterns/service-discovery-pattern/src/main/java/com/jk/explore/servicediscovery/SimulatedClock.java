package com.jk.explore.servicediscovery;

/**
 * The clock this project runs on.
 *
 * Nothing here waits for real time to pass. A remote call that "takes two
 * hundred milliseconds" advances this clock by two hundred and then returns
 * immediately. That is what lets the tests assert an exact timing and still
 * finish in a few milliseconds, and it is why no test in this project calls
 * {@code Thread.sleep}.
 */
public final class SimulatedClock {

    private long millis;

    /** Simulated milliseconds since the demo started. */
    public long millis() {
        return millis;
    }

    /** Moves simulated time forward. Only the network harness calls this. */
    public void advance(long amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("time does not run backwards");
        }
        millis += amount;
    }
}
