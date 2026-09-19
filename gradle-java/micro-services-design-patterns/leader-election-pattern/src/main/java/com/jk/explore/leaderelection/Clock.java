package com.jk.explore.leaderelection;

/** Seconds, moved only when told to. */
public class Clock {

    private long seconds;

    public long now() {
        return seconds;
    }

    public void advance(long by) {
        seconds += by;
    }
}
