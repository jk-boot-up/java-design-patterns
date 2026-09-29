package com.jk.explore.cas;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.LockSupport;

/**
 * The pattern: read the value, work out the new one, and swap it in only if nobody changed it meanwhile; if they did, try again.
 *
 * <p>{@code compareAndSet(expected, next)} is one indivisible step done by
 * the processor: "if the value is still 57, make it 56". No thread ever waits
 * for a lock; a thread that loses the race just reads again.
 */
public final class CasStock implements Stock {

    private final AtomicInteger left;
    private final AtomicLong retries = new AtomicLong();

    public CasStock(int left) {
        this.left = new AtomicInteger(left);
    }

    @Override
    public boolean buyOne() {
        while (true) {
            int seen = left.get();
            if (seen <= 0) {
                return false;
            }
            LockSupport.parkNanos(20_000);
            if (left.compareAndSet(seen, seen - 1)) {
                return true;
            }
            retries.incrementAndGet();   // someone else sold one first; look again
        }
    }

    /** The same idea in one call: the retry loop lives inside the library. */
    public boolean buyOneShort() {
        return left.getAndUpdate(s -> s > 0 ? s - 1 : s) > 0;
    }

    @Override
    public int left() {
        return left.get();
    }

    public long retries() {
        return retries.get();
    }
}
