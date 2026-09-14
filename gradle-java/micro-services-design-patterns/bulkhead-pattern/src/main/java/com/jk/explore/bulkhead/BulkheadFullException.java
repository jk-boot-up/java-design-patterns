package com.jk.explore.bulkhead;

/**
 * There was no room for this job, so it was refused rather than queued.
 *
 * A refusal sounds like a failure and is usually a mercy. The alternative — an
 * unbounded queue — accepts every job and quietly turns a thread shortage into a
 * memory problem, while callers wait for work that will not start for minutes. It is
 * better to be told "not now" in a millisecond than to be admitted to a queue that
 * is already hopeless.
 */
public class BulkheadFullException extends RuntimeException {

    private final String bulkheadName;

    public BulkheadFullException(String bulkheadName) {
        super(bulkheadName + " is full: no thread and no room in the queue");
        this.bulkheadName = bulkheadName;
    }

    public String bulkheadName() {
        return bulkheadName;
    }
}
