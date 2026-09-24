package com.jk.explore.databaseperservicecontainers;

/**
 * Counts the questions sent to a database over the network, one per query.
 *
 * <p>The count is kept by the code that sends the query, not measured, so it is the same
 * on every machine. Time is not printed anywhere in this project, because time on real
 * databases changes from run to run and from machine to machine.
 */
public final class RoundTrips {

    private int count;

    public void one() {
        count++;
    }

    public int count() {
        return count;
    }

    public void reset() {
        count = 0;
    }
}
