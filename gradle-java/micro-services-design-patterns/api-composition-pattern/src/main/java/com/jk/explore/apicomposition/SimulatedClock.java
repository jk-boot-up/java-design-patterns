package com.jk.explore.apicomposition;

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

    /**
     * Puts the clock at a given moment, forwards or backwards.
     *
     * This exists for one reason: {@link Fanout} runs its branches one after another
     * in a single thread, and each branch has to believe it left at the same moment as
     * the others. So the clock is wound back to the moment of departure before each
     * branch, and set to the slowest branch's arrival at the end. The timeline that
     * comes out is the timeline three genuinely parallel calls would have produced.
     */
    void moveTo(long moment) {
        millis = moment;
    }
}
