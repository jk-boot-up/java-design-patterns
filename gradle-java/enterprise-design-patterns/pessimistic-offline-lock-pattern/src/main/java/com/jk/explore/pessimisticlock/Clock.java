package com.jk.explore.pessimisticlock;

import java.time.Duration;

/** A clock that only moves when told to, so a lock that expires does so at exactly the moment the demo says. */
public class Clock {

    private long minutes;

    public long now() {
        return minutes;
    }

    public void advance(Duration by) {
        minutes += by.toMinutes();
    }
}
