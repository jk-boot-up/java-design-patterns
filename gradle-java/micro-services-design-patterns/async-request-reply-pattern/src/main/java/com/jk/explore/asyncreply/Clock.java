package com.jk.explore.asyncreply;

/**
 * A pretend clock in milliseconds, so the demo can show seconds of waiting without really waiting.
 */
public final class Clock {

    private long now;

    public long now() {
        return now;
    }

    public void advance(long millis) {
        now += millis;
    }
}
