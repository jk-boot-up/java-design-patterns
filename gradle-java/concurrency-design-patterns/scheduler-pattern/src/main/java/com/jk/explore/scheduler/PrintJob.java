package com.jk.explore.scheduler;

/**
 * A label to print: its order, whether it is express, and how many labels it has.
 */
public final class PrintJob {

    private final String id;
    private final boolean express;
    private final int labels;
    private final long arrived;
    int passedOver;

    public PrintJob(String id, boolean express, int labels, long arrived) {
        this.id = id;
        this.express = express;
        this.labels = labels;
        this.arrived = arrived;
    }

    public String id() {
        return id;
    }

    public boolean express() {
        return express;
    }

    public int labels() {
        return labels;
    }

    public long arrived() {
        return arrived;
    }

    @Override
    public String toString() {
        return id;
    }
}
