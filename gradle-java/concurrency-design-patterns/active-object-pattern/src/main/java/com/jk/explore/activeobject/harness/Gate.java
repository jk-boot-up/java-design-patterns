package com.jk.explore.activeobject.harness;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/**
 * <strong>Harness piece one: a door a thread waits at until the test opens
 * it.</strong>
 *
 * <p>This is how "the packing step is slow" is expressed without anybody
 * sleeping. A thread parked at a closed gate is holding exactly the way a
 * thread doing slow real work would, for precisely as long as the test
 * wants — not a guessed number of milliseconds. A sleep of any length is
 * only ever long enough until the machine running it is busy.
 *
 * <p>Copied into every project in this category rather than shared through
 * a library, so the reader of any one project sees the whole mechanism.
 */
public final class Gate {

    private final CountDownLatch latch = new CountDownLatch(1);

    /** Lets everybody waiting at the gate through, and everybody who arrives later. */
    public void open() {
        latch.countDown();
    }

    /** Waits here until the gate opens. Gives up after a generous timeout so a bug hangs a test rather than the build. */
    public void awaitOpen() {
        try {
            if (!latch.await(10, TimeUnit.SECONDS)) {
                throw new IllegalStateException("the gate was never opened");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("interrupted while waiting at the gate", e);
        }
    }

    public boolean isOpen() {
        return latch.getCount() == 0;
    }
}
