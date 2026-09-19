package com.jk.explore.claimcheck;

public class Clock {

    private long minutes;

    public long now() {
        return minutes;
    }

    public void advance(long by) {
        minutes += by;
    }
}
