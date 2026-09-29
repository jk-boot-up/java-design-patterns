package com.jk.explore.spacebased;

/**
 * Brings the database up to date in the background, a batch at a time, so no order ever waits for it.
 */
public final class DataWriter {

    private final CentralDatabase db;
    private final int batch;
    private int waiting;

    public DataWriter(CentralDatabase db, int batch) {
        this.db = db;
        this.batch = batch;
    }

    synchronized void record(int sold) {
        waiting += sold;
        if (waiting >= batch) {
            db.applyBatch(waiting);
            waiting = 0;
        }
    }

    synchronized void flush() {
        if (waiting > 0) {
            db.applyBatch(waiting);
            waiting = 0;
        }
    }
}
