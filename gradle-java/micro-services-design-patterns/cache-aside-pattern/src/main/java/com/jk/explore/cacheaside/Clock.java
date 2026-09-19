package com.jk.explore.cacheaside;

/** Seconds, moved only when told to, so an entry expires at exactly the moment the demo says. */
public class Clock {

    private long seconds;

    public long now() {
        return seconds;
    }

    public void advance(long by) {
        seconds += by;
    }
}
