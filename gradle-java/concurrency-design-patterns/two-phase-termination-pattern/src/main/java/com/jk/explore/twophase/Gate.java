package com.jk.explore.twophase;

import java.util.concurrent.CountDownLatch;

public final class Gate {

    private final CountDownLatch open = new CountDownLatch(1);

    public void await() {
        boolean interrupted = false;
        while (true) {
            try {
                open.await();
                break;
            } catch (InterruptedException e) {
                interrupted = true;
            }
        }
        if (interrupted) {
            Thread.currentThread().interrupt();
        }
    }

    public void open() {
        open.countDown();
    }
}
