package com.jk.explore.singletonspring;

import java.util.concurrent.CountDownLatch;

/** A one-shot gate: threads wait at it until it is opened. */
final class Gate {
    private final CountDownLatch latch = new CountDownLatch(1);

    void await() {
        try {
            latch.await();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    void open() {
        latch.countDown();
    }
}
