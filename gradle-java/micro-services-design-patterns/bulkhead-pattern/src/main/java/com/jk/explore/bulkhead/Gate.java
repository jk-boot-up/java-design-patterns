package com.jk.explore.bulkhead;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/**
 * A door that a job waits at until the test opens it.
 *
 * This is how "the partner API is slow" is expressed without anybody sleeping. A job
 * that is waiting at a closed gate is holding its thread exactly as a job waiting on
 * a slow network would, and it holds it for precisely as long as the test wants —
 * not a guessed number of milliseconds.
 *
 * <p>Sleeping instead would make the tests slow, and worse, flaky: a sleep of 200ms
 * is only long enough until the machine running it is busy.
 */
public final class Gate {

    private final CountDownLatch latch = new CountDownLatch(1);

    /** Lets everybody waiting at the gate through, and everybody who arrives later. */
    public void open() {
        latch.countDown();
    }

    /** Waits here until the gate opens. Gives up after a generous timeout. */
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
