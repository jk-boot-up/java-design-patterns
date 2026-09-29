package com.jk.explore.hedgedrequests;

import java.util.concurrent.Callable;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * One copy of the price service, answering after a fixed delay. Records whether its call was cancelled.
 */
public final class Replica {

    private final String name;
    private final long delayMillis;
    private final AtomicBoolean cancelled = new AtomicBoolean();

    public Replica(String name, long delayMillis) {
        this.name = name;
        this.delayMillis = delayMillis;
    }

    public Callable<String> price(String sku) {
        return () -> {
            try {
                Thread.sleep(delayMillis);
            } catch (InterruptedException e) {
                cancelled.set(true);
                throw e;
            }
            return sku + " = 19.99 from " + name;
        };
    }

    public boolean wasCancelled() {
        return cancelled.get();
    }
}
