package com.jk.explore.executearound;

public class FakeClock {

    private long now;

    public long now() {
        return now;
    }

    public void advance(long ticks) {
        now += ticks;
    }
}
