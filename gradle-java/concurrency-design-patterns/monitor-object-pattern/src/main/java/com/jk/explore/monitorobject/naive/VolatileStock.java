package com.jk.explore.monitorobject.naive;

/**
 * <strong>The popular half-fix.</strong> {@code volatile} guarantees that a
 * write is visible to other threads. It does not make "read, subtract,
 * write" one step, so the same lost update happens, exactly as before.
 * Visibility and atomicity are two different promises.
 */
public class VolatileStock {

    private volatile int count;
    private final Runnable betweenReadAndWrite;

    public VolatileStock(int initial, Runnable betweenReadAndWrite) {
        this.count = initial;
        this.betweenReadAndWrite = betweenReadAndWrite;
    }

    public void sellOne() {
        int seen = count;
        betweenReadAndWrite.run();
        count = seen - 1;
    }

    public int available() {
        return count;
    }
}
