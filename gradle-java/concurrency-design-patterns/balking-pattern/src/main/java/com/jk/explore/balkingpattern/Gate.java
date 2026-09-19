package com.jk.explore.balkingpattern;

import java.util.concurrent.CountDownLatch;

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
