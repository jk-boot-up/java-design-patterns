package com.jk.explore.spacebased;

/**
 * Without the pattern: one database that every app server asks, one query at a time, 5 ms each.
 */
public final class CentralDatabase {

    private int stock;
    private int writes;

    public CentralDatabase(int stock) {
        this.stock = stock;
    }

    public synchronized boolean takeOne() {
        SpaceBasedDemo.pause(5);
        writes++;
        if (stock <= 0) {
            return false;
        }
        stock--;
        return true;
    }

    /** Used by the background writer: one statement for a whole batch of changes. */
    public synchronized void applyBatch(int sold) {
        SpaceBasedDemo.pause(5);
        writes++;
        stock -= sold;
    }

    public synchronized int stock() {
        return stock;
    }

    public synchronized int writes() {
        return writes;
    }
}
