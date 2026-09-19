package com.jk.explore.monitorobject.naive;

/**
 * <strong>No protection at all.</strong> Selling one item is three steps —
 * read the count, work out the new count, write it back — and nothing
 * stops another thread running the same three steps in between.
 *
 * <p>{@code betweenReadAndWrite} is a hook the demo and tests use to park a
 * thread exactly in that gap. Production code would not have it; its only
 * job is to turn "sometimes wrong" into "wrong every run".
 */
public class PlainStock {

    private int count;
    private final Runnable betweenReadAndWrite;

    public PlainStock(int initial, Runnable betweenReadAndWrite) {
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
