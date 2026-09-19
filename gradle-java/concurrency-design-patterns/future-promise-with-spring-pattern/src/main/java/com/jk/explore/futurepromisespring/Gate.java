package com.jk.explore.futurepromisespring;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/** The harness's gate, copied from the partner project: a door a task waits at until the demo opens it. */
public final class Gate {

    private final CountDownLatch latch = new CountDownLatch(1);

    public void open() {
        latch.countDown();
    }

    public void awaitOpen() {
        try {
            if (!latch.await(10, TimeUnit.SECONDS)) {
                throw new IllegalStateException("the gate was never opened");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }
}
