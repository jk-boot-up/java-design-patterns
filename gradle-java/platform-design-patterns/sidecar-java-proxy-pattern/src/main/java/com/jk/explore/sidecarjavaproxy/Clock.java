package com.jk.explore.sidecarjavaproxy;

/**
 * A clock that is moved by hand rather than by the passage of time.
 *
 * <p>Nothing in this project sleeps. When a proxy waits two hundred milliseconds between
 * two attempts, the waiting is recorded by adding two hundred to a number. That is why
 * the demo finishes instantly and prints the same figures on a fast laptop and a slow
 * one, and it is why every timing quoted in these documents can be asserted by a test.
 *
 * <p>Zero always means "the moment the provider started declining", so every time
 * printed by this project is milliseconds into the trouble. That reference point is what
 * makes the two proxies comparable: the provider recovers at a fixed moment, and the
 * only question is whether an attempt arrives before it or after it.
 */
public final class Clock {

    private long millis;

    public long now() {
        return millis;
    }

    /** Records a wait without performing one. */
    public void waitFor(long forMillis) {
        millis += forMillis;
    }

    public void reset() {
        millis = 0;
    }
}
