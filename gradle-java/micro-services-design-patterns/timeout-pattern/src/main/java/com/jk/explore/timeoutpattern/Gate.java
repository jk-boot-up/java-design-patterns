package com.jk.explore.timeoutpattern;

import java.util.concurrent.CountDownLatch;

/** Holds a call for as long as the demo likes, so "a supplier that never answers" is exact. */
public final class Gate {

    private final CountDownLatch open = new CountDownLatch(1);

    public void await() {
        try {
            open.await();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    public void open() {
        open.countDown();
    }
}
