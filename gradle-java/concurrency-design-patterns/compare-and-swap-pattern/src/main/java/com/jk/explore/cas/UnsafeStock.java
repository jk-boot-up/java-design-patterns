package com.jk.explore.cas;

import java.util.concurrent.locks.LockSupport;

/**
 * Without the pattern: check, then act, with nothing stopping two buyers checking at the same moment.
 */
public final class UnsafeStock implements Stock {

    private int left;

    public UnsafeStock(int left) {
        this.left = left;
    }

    @Override
    public boolean buyOne() {
        int seen = left;
        if (seen <= 0) {
            return false;
        }
        LockSupport.parkNanos(20_000);   // a fraud check between looking and taking
        left = seen - 1;
        return true;
    }

    @Override
    public int left() {
        return left;
    }
}
