package com.jk.explore.servicemesh;

/** The payment service on a bad day: it refuses the first few calls, then works. */
public class Flaky implements Backend {

    private final int refusals;
    private int received;

    public Flaky(int refusals) {
        this.refusals = refusals;
    }

    @Override
    public boolean call() {
        received++;
        return received > refusals;
    }

    @Override
    public int received() {
        return received;
    }
}
