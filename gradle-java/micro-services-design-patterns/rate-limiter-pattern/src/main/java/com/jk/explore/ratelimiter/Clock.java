package com.jk.explore.ratelimiter;

/** Milliseconds, moved only when told to. */
public class Clock {

    private long millis;

    public long now() {
        return millis;
    }

    public void advance(long by) {
        millis += by;
    }
}
