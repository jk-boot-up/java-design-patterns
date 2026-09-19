package com.jk.explore.executearound;

import java.util.function.Supplier;

/** Execute around, for measuring. The same wrapper suits any work. */
public class Timed {

    private final FakeClock clock;
    private long lastTicks;

    public Timed(FakeClock clock) {
        this.clock = clock;
    }

    public <T> T around(Supplier<T> work) {
        long start = clock.now();
        try {
            return work.get();
        } finally {
            lastTicks = clock.now() - start;
        }
    }

    public long lastTicks() {
        return lastTicks;
    }
}
