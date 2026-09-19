package com.jk.explore.timeoutpattern;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * The supplier's stock API. It can be held at a gate, and it counts the calls that started and the
 * calls that finished the work, whether or not anyone was still waiting for the answer.
 */
public class SupplierApi {

    private final Gate gate;
    private final AtomicInteger started = new AtomicInteger();
    private final AtomicInteger finished = new AtomicInteger();

    public SupplierApi(Gate gate) {
        this.gate = gate;
    }

    public String stockOf(String sku) {
        started.incrementAndGet();
        gate.await();
        finished.incrementAndGet();
        return "42 of " + sku;
    }

    public int started() {
        return started.get();
    }

    public int finished() {
        return finished.get();
    }
}
