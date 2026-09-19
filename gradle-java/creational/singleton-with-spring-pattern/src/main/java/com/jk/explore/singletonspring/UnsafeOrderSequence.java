package com.jk.explore.singletonspring;

/**
 * A sequencer whose counter is a plain long. As a Spring singleton it is shared by every
 * thread, and Spring does nothing to protect it. The pause hook lets a demo hold one
 * thread between the read and the write, so the collision happens every time.
 */
public class UnsafeOrderSequence {

    private long counter;

    public String nextOrderNumber(Runnable pauseBetweenReadAndWrite) {
        long next = counter + 1;
        pauseBetweenReadAndWrite.run();
        counter = next;
        return String.format("ORD-%06d", next);
    }
}
