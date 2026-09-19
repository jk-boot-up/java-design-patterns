package com.jk.explore.bulkheadr4j;

import java.util.concurrent.CountDownLatch;

/**
 * Holds calls in flight so the demo can look at the compartments while they are full.
 * Every call announces it has arrived, then waits until the gate is opened.
 */
public final class Gate {

    private final CountDownLatch arrivals;
    private final CountDownLatch open = new CountDownLatch(1);

    public Gate(int expectedArrivals) {
        this.arrivals = new CountDownLatch(expectedArrivals);
    }

    void arriveAndWait() {
        arrivals.countDown();
        await(open);
    }

    public void awaitArrivals() {
        await(arrivals);
    }

    public void open() {
        open.countDown();
    }

    private static void await(CountDownLatch latch) {
        try {
            latch.await();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }
}
