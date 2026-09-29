package com.jk.explore.backpressure;

/**
 * A supplier's product feed (1,000 products a second) into the search indexer (100 a second), second by second.
 */
public final class FeedSimulation {

    public static final int SUPPLIER_PER_SECOND = 1000;
    public static final int INDEXER_PER_SECOND = 100;

    public record Result(int seconds, int indexed, int maxWaiting, int finalWaiting) {
    }

    /** Runs until all products are sent and indexed, or {@code limitSeconds} pass. {@code capacity} 0 means unbounded. */
    public static Result run(int products, int capacity, int limitSeconds) {
        int sent = 0;
        int waiting = 0;
        int indexed = 0;
        int maxWaiting = 0;
        int second = 0;
        while (second < limitSeconds && indexed < products) {
            int canSend = Math.min(SUPPLIER_PER_SECOND, products - sent);
            if (capacity > 0) {
                canSend = Math.min(canSend, capacity - waiting);   // the producer is made to wait
            }
            sent += canSend;
            waiting += canSend;
            maxWaiting = Math.max(maxWaiting, waiting);
            int done = Math.min(INDEXER_PER_SECOND, waiting);
            waiting -= done;
            indexed += done;
            second++;
        }
        return new Result(second, indexed, maxWaiting, waiting);
    }

    private FeedSimulation() {
    }
}
